from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List


def parse_entries(text: str) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    current: Dict[str, Any] | None = None
    for line in text.splitlines():
        region = re.match(r"\s*-\s+country_or_region:\s*(.+)", line)
        if region:
            if current:
                entries.append(current)
            current = {"country_or_region": region.group(1).strip().strip('"')}
            continue
        verified = re.match(r"\s+last_verified:\s*['\"]?([0-9]{4}-[0-9]{2}-[0-9]{2})['\"]?", line)
        if verified and current is not None:
            current["last_verified"] = verified.group(1)
    if current:
        entries.append(current)
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether crisis-resource starter entries need re-verification.")
    parser.add_argument("--file", default="references/crisis-resources.md")
    parser.add_argument("--max-age-days", type=int, default=90)
    args = parser.parse_args()

    path = Path(args.file)
    text = path.read_text(encoding="utf-8-sig")
    today = date.today()
    stale: List[Dict[str, Any]] = []
    entries = parse_entries(text)
    for entry in entries:
        raw = entry.get("last_verified")
        if not raw:
            entry["reason"] = "missing last_verified"
            stale.append(entry)
            continue
        verified = datetime.strptime(str(raw), "%Y-%m-%d").date()
        age_days = (today - verified).days
        entry["age_days"] = age_days
        if age_days > args.max_age_days:
            stale.append(entry)

    report = {
        "status": "stale" if stale else "ok",
        "file": str(path),
        "checked_entries": len(entries),
        "max_age_days": args.max_age_days,
        "stale_entries": stale,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
