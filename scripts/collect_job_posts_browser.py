from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

from _local_data import JOB_POSTS_CACHE_DEFAULT, ensure_data_dir, now_iso, read_json, truthy, write_json


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _load_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_raw_records(path: Path) -> List[Dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return _load_jsonl(path)
    if suffix == ".csv":
        return _load_csv(path)
    if suffix == ".json":
        value = _load_json(path)
        if isinstance(value, dict) and isinstance(value.get("posts"), list):
            return [item for item in value["posts"] if isinstance(item, dict)]
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            return [value]
    raise SystemExit(f"Unsupported input format: {suffix}. Use .json/.jsonl/.csv")


def listify(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    for sep in [";", "|", "，", ",", "、"]:
        if sep in text:
            return [part.strip() for part in text.split(sep) if part.strip()]
    return [text]


def clean(value: Any) -> str:
    return str(value or "").strip()


def normalize_record(raw: Dict[str, Any], fallback_source: str) -> Dict[str, Any]:
    captured_at = clean(raw.get("captured_at")) or now_iso()
    try:
        datetime.fromisoformat(captured_at)
    except ValueError:
        captured_at = now_iso()

    return {
        "title": clean(raw.get("title") or raw.get("job_title") or raw.get("position") or "待核验"),
        "company": clean(raw.get("company") or raw.get("company_name") or "待核验"),
        "city": clean(raw.get("city") or raw.get("location") or "待核验"),
        "salary": clean(raw.get("salary") or raw.get("pay") or ""),
        "experience": clean(raw.get("experience") or raw.get("experience_level") or ""),
        "education": clean(raw.get("education") or raw.get("degree") or ""),
        "skills": listify(raw.get("skills") or raw.get("skill_requirements") or raw.get("keywords")),
        "responsibilities": listify(raw.get("responsibilities") or raw.get("job_desc") or raw.get("description")),
        "benefits": listify(raw.get("benefits") or raw.get("welfare") or raw.get("perks")),
        "risk_signals": listify(raw.get("risk_signals") or raw.get("risk") or raw.get("warnings")),
        "source_url": clean(raw.get("source_url") or raw.get("url") or raw.get("link") or fallback_source),
        "captured_at": captured_at,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Store browser-collected job posts into local cache JSON.")
    parser.add_argument("--input", help="Raw records file (.json/.jsonl/.csv).")
    parser.add_argument("--query", default="", help="Search query used for collection.")
    parser.add_argument("--source", default="browser", help="Collection source label.")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--append", action="store_true", help="Append to existing cache instead of replacing.")
    parser.add_argument("--consent", default="", help="Must be true/yes to confirm saving job-search data locally when --input is provided.")
    args = parser.parse_args()

    root = ensure_data_dir(args.data_dir)
    cache_path = root / "job_posts_cache.json"

    existing = read_json(cache_path, JOB_POSTS_CACHE_DEFAULT)
    if not isinstance(existing, dict):
        existing = dict(JOB_POSTS_CACHE_DEFAULT)

    records: List[Dict[str, Any]] = []
    if args.input:
        if not truthy(args.consent):
            raise SystemExit("Refusing to save job posts: --consent must be true when --input is provided.")
        input_path = Path(args.input).expanduser().resolve()
        if not input_path.exists():
            raise SystemExit(f"Input file not found: {input_path}")
        raw_records = load_raw_records(input_path)
        records = [normalize_record(raw, fallback_source=args.source) for raw in raw_records]
    else:
        print(
            json.dumps(
                {
                    "status": "needs_input",
                    "message": "No input provided. Provide --input from browser automation export.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    posts = records if not args.append else list(existing.get("posts", [])) + records
    payload = {
        "version": 1,
        "updated_at": now_iso(),
        "source": args.source,
        "query": args.query,
        "posts": posts,
    }

    write_json(cache_path, payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "file": str(cache_path),
                "new_records": len(records),
                "total_records": len(posts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
