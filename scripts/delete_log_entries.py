from __future__ import annotations

import argparse
import json

from _local_data import CONTACT_FIELDS, DAILY_FIELDS, EVENT_FIELDS, ensure_data_dir, read_rows, write_rows


TARGETS = {
    "event": ("event_log.csv", EVENT_FIELDS),
    "daily": ("daily_summary.csv", DAILY_FIELDS),
    "contacts": ("support_contacts.csv", CONTACT_FIELDS),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Delete specific local records by explicit user request.")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--target", choices=TARGETS.keys(), required=True)
    parser.add_argument("--date", help="Delete rows matching this YYYY-MM-DD date for event/daily logs.")
    parser.add_argument("--name", help="Delete support contact by name_or_alias.")
    args = parser.parse_args()

    root = ensure_data_dir(args.data_dir)
    filename, fields = TARGETS[args.target]
    path = root / filename
    rows = read_rows(path)

    if args.target in {"event", "daily"}:
        if not args.date:
            raise SystemExit("--date is required for event/daily deletions.")
        kept = [row for row in rows if row.get("date") != args.date]
    else:
        if not args.name:
            raise SystemExit("--name is required for contact deletions.")
        kept = [row for row in rows if row.get("name_or_alias") != args.name]

    write_rows(path, fields, kept)
    print(json.dumps({"file": str(path), "deleted": len(rows) - len(kept)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
