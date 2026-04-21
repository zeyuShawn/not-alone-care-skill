from __future__ import annotations

import argparse
import json

from _local_data import DAILY_FIELDS, append_row, ensure_data_dir, now_parts, parse_fields, truthy


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a consented daily summary.")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--field", action="append", default=[], help="key=value field. Repeat as needed.")
    args = parser.parse_args()

    row = parse_fields(args.field)
    if not truthy(row.get("save_consent")):
        raise SystemExit("Refusing to save: save_consent=true is required.")

    date, _ = now_parts()
    row.setdefault("date", date)

    root = ensure_data_dir(args.data_dir)
    append_row(root / "daily_summary.csv", DAILY_FIELDS, row)
    print(json.dumps({"file": str(root / "daily_summary.csv"), "status": "appended"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
