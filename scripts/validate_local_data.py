from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List

from _local_data import (
    CAREER_PROFILE_DEFAULT,
    CONTACT_FIELDS,
    DAILY_FIELDS,
    EVENT_FIELDS,
    JOB_POSTS_CACHE_DEFAULT,
    OUTING_PREFERENCES_DEFAULT,
    ensure_data_dir,
    read_json,
    read_rows,
    validate_daily_row,
    validate_event_row,
)

JSON_STORES = {
    "outing_preferences.json": OUTING_PREFERENCES_DEFAULT,
    "career_profile.json": CAREER_PROFILE_DEFAULT,
    "job_posts_cache.json": JOB_POSTS_CACHE_DEFAULT,
}


def header_issues(name: str, rows: List[Dict[str, str]], expected_fields: List[str]) -> List[str]:
    if not rows:
        return []
    actual = set(rows[0].keys())
    expected = set(expected_fields)
    issues: List[str] = []
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        issues.append(f"{name} missing field(s): {', '.join(missing)}")
    if extra:
        issues.append(f"{name} unknown field(s): {', '.join(extra)}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local mental-care data files without diagnosis.")
    parser.add_argument("--data-dir", default=None)
    args = parser.parse_args()

    root = ensure_data_dir(args.data_dir)
    issues: List[str] = []
    meta: Dict[str, Any] = {}

    event_rows = read_rows(root / "event_log.csv")
    daily_rows = read_rows(root / "daily_summary.csv")
    contact_rows = read_rows(root / "support_contacts.csv")
    meta.update({"event_rows": len(event_rows), "daily_rows": len(daily_rows), "contact_rows": len(contact_rows)})

    issues.extend(header_issues("event_log.csv", event_rows, EVENT_FIELDS))
    issues.extend(header_issues("daily_summary.csv", daily_rows, DAILY_FIELDS))
    issues.extend(header_issues("support_contacts.csv", contact_rows, CONTACT_FIELDS))

    for idx, row in enumerate(event_rows, start=2):
        try:
            validate_event_row(row)
        except ValueError as exc:
            issues.append(f"event_log.csv line {idx}: {exc}")
    for idx, row in enumerate(daily_rows, start=2):
        try:
            validate_daily_row(row)
        except ValueError as exc:
            issues.append(f"daily_summary.csv line {idx}: {exc}")

    for filename, default in JSON_STORES.items():
        try:
            payload = read_json(root / filename, default)
        except ValueError as exc:
            issues.append(str(exc))
            continue
        if not isinstance(payload, dict):
            issues.append(f"{filename} root must be object")
        elif "version" not in payload:
            issues.append(f"{filename} missing version")

    report = {"status": "failed" if issues else "ok", "data_dir": str(root), "issues": issues, "meta": meta}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
