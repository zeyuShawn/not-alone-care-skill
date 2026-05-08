from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

from _local_data import ensure_data_dir, now_iso, truthy, write_json


def clean(value: Any) -> str:
    return str(value or "").strip()


def listify(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [clean(v) for v in value if clean(v)]
    text = clean(value)
    if not text:
        return []
    for sep in [";", "|", "，", ",", "、", "\n"]:
        if sep in text:
            return [part.strip() for part in text.split(sep) if part.strip()]
    return [text]


def load_json(path: Path) -> List[Dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(payload, dict):
        if isinstance(payload.get("posts"), list):
            return [item for item in payload["posts"] if isinstance(item, dict)]
        return [payload]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            rows.append(value)
    return rows


def load_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse_text_block(block: str) -> Dict[str, Any]:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        return {}

    text = "\n".join(lines)

    def first_match(patterns: Iterable[str], default: str = "") -> str:
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return clean(match.group(1))
        return default

    title = first_match(
        [
            r"(?:职位|岗位|Title|Position)\s*[:：]\s*(.+)",
        ],
        default=lines[0],
    )

    company = first_match([r"(?:公司|Company)\s*[:：]\s*(.+)"])
    city = first_match([r"(?:城市|地点|Location|City)\s*[:：]\s*(.+)"])
    salary = first_match([r"(?:薪资|薪酬|Salary|Pay)\s*[:：]\s*(.+)"])
    experience = first_match([r"(?:经验|Experience)\s*[:：]\s*(.+)"])
    education = first_match([r"(?:学历|Education)\s*[:：]\s*(.+)"])
    url = first_match([r"https?://\S+"])

    skills_raw = first_match([r"(?:技能|要求|Skills?)\s*[:：]\s*(.+)"])
    responsibilities_raw = first_match([r"(?:职责|Description|Responsibilit(?:y|ies))\s*[:：]\s*(.+)"])
    benefits_raw = first_match([r"(?:福利|Benefits?)\s*[:：]\s*(.+)"])

    return {
        "title": title or "待核验",
        "company": company or "待核验",
        "city": city or "待核验",
        "salary": salary,
        "experience": experience,
        "education": education,
        "skills": listify(skills_raw),
        "responsibilities": listify(responsibilities_raw),
        "benefits": listify(benefits_raw),
        "risk_signals": [],
        "source_url": url,
        "captured_at": now_iso(),
    }


def strip_html(text: str) -> str:
    without_script = re.sub(r"<script.*?>.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    without_style = re.sub(r"<style.*?>.*?</style>", " ", without_script, flags=re.IGNORECASE | re.DOTALL)
    plain = re.sub(r"<[^>]+>", "\n", without_style)
    plain = re.sub(r"\n{3,}", "\n\n", plain)
    return plain


def load_text_like(path: Path) -> List[Dict[str, Any]]:
    raw = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".html", ".htm"}:
        raw = strip_html(raw)

    blocks = [block.strip() for block in re.split(r"\n\s*\n", raw) if block.strip()]
    parsed = [parse_text_block(block) for block in blocks]
    return [item for item in parsed if item]


def normalize_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title": clean(raw.get("title") or raw.get("job_title") or raw.get("position") or "待核验"),
        "company": clean(raw.get("company") or raw.get("company_name") or "待核验"),
        "city": clean(raw.get("city") or raw.get("location") or "待核验"),
        "salary": clean(raw.get("salary") or raw.get("pay") or ""),
        "experience": clean(raw.get("experience") or raw.get("experience_level") or ""),
        "education": clean(raw.get("education") or raw.get("degree") or ""),
        "skills": listify(raw.get("skills") or raw.get("skill_requirements")),
        "responsibilities": listify(raw.get("responsibilities") or raw.get("description") or raw.get("job_desc")),
        "benefits": listify(raw.get("benefits") or raw.get("welfare") or raw.get("perks")),
        "risk_signals": listify(raw.get("risk_signals") or raw.get("risk") or raw.get("warnings")),
        "source_url": clean(raw.get("source_url") or raw.get("url") or raw.get("link") or ""),
        "captured_at": clean(raw.get("captured_at")) or now_iso(),
    }


def load_any(path: Path) -> List[Dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_json(path)
    if suffix == ".jsonl":
        return load_jsonl(path)
    if suffix == ".csv":
        return load_csv(path)
    if suffix in {".txt", ".md", ".html", ".htm"}:
        return load_text_like(path)
    raise SystemExit(f"Unsupported input format: {suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize job posts into standard JSON schema.")
    parser.add_argument("--input", required=True, help="Input file (.json/.jsonl/.csv/.txt/.md/.html).")
    parser.add_argument("--output", default=None, help="Output JSON path. Defaults to stdout only.")
    parser.add_argument("--data-dir", default=None, help="Data root for --save-cache mode.")
    parser.add_argument("--save-cache", action="store_true", help="Save normalized result to job_posts_cache.json.")
    parser.add_argument("--consent", default="", help="Required as true/yes when --save-cache writes job-search data locally.")
    parser.add_argument("--source", default="browser")
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")

    raw_records = load_any(in_path)
    normalized = [normalize_record(row) for row in raw_records]

    payload = {
        "version": 1,
        "updated_at": now_iso(),
        "source": args.source,
        "query": args.query,
        "posts": normalized,
    }

    if args.output:
        out_path = Path(args.output).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.save_cache:
        if not truthy(args.consent):
            raise SystemExit("Refusing to save job posts cache: --consent must be true when --save-cache is used.")
        root = ensure_data_dir(args.data_dir)
        write_json(root / "job_posts_cache.json", payload)

    print(
        json.dumps(
            {
                "status": "ok",
                "input": str(in_path),
                "output": str(Path(args.output).expanduser().resolve()) if args.output else None,
                "count": len(normalized),
                "saved_cache": bool(args.save_cache),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
