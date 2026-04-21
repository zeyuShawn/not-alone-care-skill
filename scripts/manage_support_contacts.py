from __future__ import annotations

import argparse
import json

from _local_data import CONTACT_FIELDS, append_row, ensure_data_dir, parse_fields, read_rows, truthy, write_rows


def add_contact(data_dir: str | None, fields: list[str]) -> int:
    row = parse_fields(fields)
    if not row.get("name_or_alias"):
        raise SystemExit("name_or_alias is required.")
    if not truthy(row.get("consent_to_use")):
        raise SystemExit("Refusing to save contact: consent_to_use=true is required.")
    root = ensure_data_dir(data_dir)
    append_row(root / "support_contacts.csv", CONTACT_FIELDS, row)
    print(json.dumps({"file": str(root / "support_contacts.csv"), "status": "added"}, ensure_ascii=False))
    return 0


def list_contacts(data_dir: str | None) -> int:
    root = ensure_data_dir(data_dir)
    rows = read_rows(root / "support_contacts.csv")
    safe_rows = [
        {k: v for k, v in row.items() if k != "contact_method"}
        for row in rows
        if truthy(row.get("consent_to_use"))
    ]
    print(json.dumps(safe_rows, ensure_ascii=False, indent=2))
    return 0


def show_contact(data_dir: str | None, name: str, include_contact_method: bool) -> int:
    root = ensure_data_dir(data_dir)
    rows = read_rows(root / "support_contacts.csv")
    matches = [
        row for row in rows
        if row.get("name_or_alias") == name and truthy(row.get("consent_to_use"))
    ]
    if not matches:
        print(json.dumps({"status": "not_found", "name_or_alias": name}, ensure_ascii=False))
        return 0

    row = dict(matches[0])
    if not include_contact_method:
        row.pop("contact_method", None)
    print(json.dumps(row, ensure_ascii=False, indent=2))
    return 0


def delete_contact(data_dir: str | None, name: str) -> int:
    root = ensure_data_dir(data_dir)
    path = root / "support_contacts.csv"
    rows = read_rows(path)
    kept = [row for row in rows if row.get("name_or_alias") != name]
    write_rows(path, CONTACT_FIELDS, kept)
    print(json.dumps({"file": str(path), "deleted": len(rows) - len(kept)}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage local support contacts.")
    parser.add_argument("--data-dir", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add")
    add.add_argument("--field", action="append", default=[], help="key=value field. Repeat as needed.")

    sub.add_parser("list")

    show = sub.add_parser("show")
    show.add_argument("--name", required=True)
    show.add_argument(
        "--include-contact-method",
        action="store_true",
        help="Reveal contact_method only after the user explicitly agrees.",
    )

    delete = sub.add_parser("delete")
    delete.add_argument("--name", required=True)

    args = parser.parse_args()
    if args.command == "add":
        return add_contact(args.data_dir, args.field)
    if args.command == "list":
        return list_contacts(args.data_dir)
    if args.command == "show":
        return show_contact(args.data_dir, args.name, args.include_contact_method)
    if args.command == "delete":
        return delete_contact(args.data_dir, args.name)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
