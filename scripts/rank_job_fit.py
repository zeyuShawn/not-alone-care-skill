from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

from _local_data import ensure_data_dir, now_iso


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise SystemExit(f"Expected JSON object: {path}")
    return value


def tokenize(text: str) -> List[str]:
    text = text.lower()
    parts = re.split(r"[^a-z0-9\u4e00-\u9fa5+#]+", text)
    return [part for part in parts if part and len(part) > 1]


def to_token_set(values: Iterable[str]) -> Set[str]:
    tokens: Set[str] = set()
    for value in values:
        tokens.update(tokenize(str(value)))
    return tokens


def listify(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    for sep in [";", "|", "，", ",", "、", "\n"]:
        if sep in text:
            return [part.strip() for part in text.split(sep) if part.strip()]
    return [text]


def classify(score: float, risk_hit: bool) -> str:
    if score >= 0.65 and not risk_hit:
        return "稳妥尝试"
    if score >= 0.4:
        return "值得补差"
    return "暂不建议"


def low_burden_action(category: str, title: str) -> str:
    if category == "稳妥尝试":
        return f"收藏岗位《{title}》，并准备一版 3 行项目证据后尝试投递。"
    if category == "值得补差":
        return f"先收藏《{title}》，补一个最小 demo 或简历段落后再评估。"
    return f"将《{title}》标记为暂缓，记录不匹配原因并转向更稳妥岗位。"


def risk_signal_hit(signals: Iterable[str], constraints: Dict[str, str]) -> bool:
    merged = " ".join(signals).lower()
    high_load_tokens = ["加班", "996", "night shift", "high pressure", "销售指标", "出差频繁"]
    if any(token.lower() in merged for token in high_load_tokens):
        return True
    energy_limit = str(constraints.get("energy_load_limit", "")).strip().lower()
    if energy_limit and energy_limit in {"low", "低", "轻负担", "low_load"}:
        if any(token.lower() in merged for token in ["high pressure", "996", "加班"]):
            return True
    return False


def normalize_post(post: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title": str(post.get("title") or "待核验岗位").strip(),
        "company": str(post.get("company") or "待核验公司").strip(),
        "city": str(post.get("city") or "").strip(),
        "salary": str(post.get("salary") or "").strip(),
        "experience": str(post.get("experience") or "").strip(),
        "education": str(post.get("education") or "").strip(),
        "skills": listify(post.get("skills")),
        "responsibilities": listify(post.get("responsibilities")),
        "benefits": listify(post.get("benefits")),
        "risk_signals": listify(post.get("risk_signals")),
        "source_url": str(post.get("source_url") or "").strip(),
        "captured_at": str(post.get("captured_at") or "").strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank job fit using career profile + normalized job posts.")
    parser.add_argument("--profile", default=None, help="career_profile.json path.")
    parser.add_argument("--posts", default=None, help="job posts JSON path.")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--output", default=None, help="Optional output JSON file path.")
    args = parser.parse_args()

    root = ensure_data_dir(args.data_dir)
    profile_path = Path(args.profile).expanduser().resolve() if args.profile else root / "career_profile.json"
    posts_path = Path(args.posts).expanduser().resolve() if args.posts else root / "job_posts_cache.json"

    if not profile_path.exists():
        raise SystemExit(f"Profile file not found: {profile_path}")
    if not posts_path.exists():
        raise SystemExit(f"Posts file not found: {posts_path}")

    profile = load_json(profile_path)
    posts_payload = load_json(posts_path)
    posts_raw = posts_payload.get("posts", [])
    if not isinstance(posts_raw, list):
        raise SystemExit("`posts` must be a list in posts JSON.")

    evidenced_skills = [str(item) for item in profile.get("skills_evidenced", [])]
    target_roles = [str(item) for item in profile.get("target_roles", [])]
    constraints = profile.get("constraints", {}) if isinstance(profile.get("constraints"), dict) else {}

    evidence_tokens = to_token_set(evidenced_skills + target_roles)

    ranking: List[Dict[str, Any]] = []
    for raw in posts_raw:
        if not isinstance(raw, dict):
            continue
        post = normalize_post(raw)

        requirement_tokens = to_token_set(post["skills"] + post["responsibilities"] + [post["title"]])
        if not requirement_tokens:
            requirement_tokens = to_token_set([post["title"]])

        overlap_tokens = sorted(evidence_tokens.intersection(requirement_tokens))
        gap_tokens = sorted(requirement_tokens.difference(evidence_tokens))

        overlap_score = len(overlap_tokens) / max(1, len(requirement_tokens))
        risk_hit = risk_signal_hit(post["risk_signals"], constraints)

        final_score = max(0.0, round(overlap_score - (0.15 if risk_hit else 0.0), 4))
        category = classify(final_score, risk_hit)

        reason_bits = []
        if overlap_tokens:
            reason_bits.append(f"已有证据覆盖 {len(overlap_tokens)} 项关键要求")
        else:
            reason_bits.append("当前证据覆盖较少")
        if gap_tokens:
            reason_bits.append(f"主要缺口: {', '.join(gap_tokens[:5])}")
        if risk_hit:
            reason_bits.append("风险信号与当前承受上限可能不匹配")

        ranking.append(
            {
                "title": post["title"],
                "company": post["company"],
                "category": category,
                "score": final_score,
                "reason": "；".join(reason_bits),
                "overlap_tokens": overlap_tokens[:12],
                "gap_tokens": gap_tokens[:12],
                "risk_signals": post["risk_signals"],
                "next_action": low_burden_action(category, post["title"]),
                "source_url": post["source_url"],
            }
        )

    def sort_key(item: Dict[str, Any]) -> tuple:
        order = {"稳妥尝试": 0, "值得补差": 1, "暂不建议": 2}
        return (order.get(str(item.get("category")), 3), -float(item.get("score", 0.0)))

    ranking.sort(key=sort_key)

    output = {
        "version": 1,
        "generated_at": now_iso(),
        "profile_file": str(profile_path),
        "posts_file": str(posts_path),
        "summary": {
            "稳妥尝试": sum(1 for item in ranking if item["category"] == "稳妥尝试"),
            "值得补差": sum(1 for item in ranking if item["category"] == "值得补差"),
            "暂不建议": sum(1 for item in ranking if item["category"] == "暂不建议"),
            "total": len(ranking),
        },
        "ranking": ranking,
        "note": "结果为辅助判断，不是客观定论。请结合真实投递与面试反馈持续校正。",
    }

    if args.output:
        out_path = Path(args.output).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
