from __future__ import annotations

import argparse
import json
from datetime import datetime

from _local_data import CONTACT_FIELDS, DAILY_FIELDS, EVENT_FIELDS, ensure_data_dir, read_rows, write_rows

TARGETS = {
    "event": ("event_log.csv", EVENT_FIELDS),
    "daily": ("daily_summary.csv", DAILY_FIELDS),
    "contacts": ("support_contacts.csv", CONTACT_FIELDS),
}


def parse_date(value: str, name: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit(f"{name} must use YYYY-MM-DD format.") from exc


def in_date_scope(row_date: str, exact: str | None, from_date: str | None, to_date: str | None, delete_all: bool) -> bool:
    if delete_all:
        return True
    if exact:
        return row_date == exact
    if from_date or to_date:
        if not row_date:
            return False
        current = parse_date(row_date, "row date")
        if from_date and current < parse_date(from_date, "--from-date"):
            return False
        if to_date and current > parse_date(to_date, "--to-date"):
            return False
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Delete specific local records by explicit user request.")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--target", choices=TARGETS.keys(), required=True)
    parser.add_argument("--date", help="Delete rows matching this YYYY-MM-DD date for event/daily logs.")
    parser.add_argument("--from-date", help="Delete event/daily rows on or after this YYYY-MM-DD date.")
    parser.add_argument("--to-date", help="Delete event/daily rows on or before this YYYY-MM-DD date.")
    parser.add_argument("--all", action="store_true", help="Delete all rows for the selected target.")
    parser.add_argument("--name", help="Delete support contact by name_or_alias.")
    parser.add_argument("--dry-run", action="store_true", help="Report matching rows without changing files.")
    parser.add_argument("--confirm", default="", help="Must be YES for destructive deletes unless --dry-run is used.")
    args = parser.parse_args()

    if args.confirm != "YES" and not args.dry_run:
        raise SystemExit("Refusing delete: pass --confirm YES, or use --dry-run to preview.")

    if args.date and (args.from_date or args.to_date):
        raise SystemExit("Use either --date or --from-date/--to-date, not both.")

    root = ensure_data_dir(args.data_dir)
    filename, fields = TARGETS[args.target]
    path = root / filename
    rows = read_rows(path)

    if args.target in {"event", "daily"}:
        if not (args.date or args.from_date or args.to_date or args.all):
            raise SystemExit("Provide --date, --from-date/--to-date, or --all for event/daily deletions.")
        kept = [row for row in rows if not in_date_scope(row.get("date", ""), args.date, args.from_date, args.to_date, args.all)]
    else:
        if args.all:
            kept = []
        else:
            if not args.name:
                raise SystemExit("--name or --all is required for contact deletions.")
            kept = [row for row in rows if row.get("name_or_alias") != args.name]

    deleted = len(rows) - len(kept)
    if not args.dry_run:
        write_rows(path, fields, kept)

    print(
        json.dumps(
            {"file": str(path), "matched": deleted, "deleted": 0 if args.dry_run else deleted, "dry_run": bool(args.dry_run)},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
