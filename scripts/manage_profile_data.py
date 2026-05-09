from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

from _local_data import (
    CAREER_PROFILE_DEFAULT,
    JOB_POSTS_CACHE_DEFAULT,
    OUTING_PREFERENCES_DEFAULT,
    ensure_data_dir,
    now_iso,
    read_json,
    truthy,
    write_json,
)

STORE_DEFAULTS = {
    "outing": ("outing_preferences.json", OUTING_PREFERENCES_DEFAULT),
    "career": ("career_profile.json", CAREER_PROFILE_DEFAULT),
    "jobs": ("job_posts_cache.json", JOB_POSTS_CACHE_DEFAULT),
}


def require_write_consent(store_key: str, consent: str) -> None:
    if not truthy(consent):
        raise SystemExit(f"Refusing to modify {store_key} store: pass --consent true after explicit user consent.")


def set_nested(obj: Dict[str, Any], key_path: str, value: Any) -> None:
    keys = [k for k in key_path.split(".") if k]
    if not keys:
        raise ValueError("Empty key path")
    target = obj
    for key in keys[:-1]:
        if key not in target or not isinstance(target[key], dict):
            target[key] = {}
        target = target[key]
    target[keys[-1]] = value


def del_nested(obj: Dict[str, Any], key_path: str) -> bool:
    keys = [k for k in key_path.split(".") if k]
    if not keys:
        return False
    target = obj
    for key in keys[:-1]:
        value = target.get(key)
        if not isinstance(value, dict):
            return False
        target = value
    return target.pop(keys[-1], None) is not None


def parse_value(raw: str) -> Any:
    raw = raw.strip()
    if raw.lower() in {"true", "false", "null"}:
        return json.loads(raw.lower())
    try:
        if raw.startswith("{") or raw.startswith("[") or raw.startswith('"'):
            return json.loads(raw)
    except json.JSONDecodeError:
        pass
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        return raw


def resolve_store(root: Path, store_key: str) -> tuple[Path, Dict[str, Any]]:
    filename, default = STORE_DEFAULTS[store_key]
    return root / filename, default


def main() -> int:
    parser = argparse.ArgumentParser(description="View/update/delete ver2 JSON stores.")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--store", choices=STORE_DEFAULTS.keys(), required=True)

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("show")

    update = sub.add_parser("update")
    update.add_argument("--set", action="append", default=[], help="dot.path=value, repeatable")
    update.add_argument("--consent", default="", help="Required as true/yes after explicit user consent for any write.")

    delete = sub.add_parser("delete")
    delete.add_argument("--key", action="append", default=[], help="dot.path to delete, repeatable")
    delete.add_argument("--consent", default="", help="Required as true/yes after explicit user consent for any write.")

    reset = sub.add_parser("reset")
    reset.add_argument("--confirm", required=True, help="Must be YES to reset store")

    args = parser.parse_args()

    root = ensure_data_dir(args.data_dir)
    path, default = resolve_store(root, args.store)
    payload = read_json(path, default)
    if not isinstance(payload, dict):
        payload = dict(default)

    if args.command == "show":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.command == "update":
        require_write_consent(args.store, args.consent)
        if not args.set:
            raise SystemExit("No updates provided. Use --set key=value")
        for item in args.set:
            if "=" not in item:
                raise SystemExit(f"Invalid --set item: {item}")
            key, value = item.split("=", 1)
            set_nested(payload, key.strip(), parse_value(value))
        payload["updated_at"] = now_iso()
        write_json(path, payload)
        print(json.dumps({"status": "ok", "file": str(path), "updated": len(args.set)}, ensure_ascii=False, indent=2))
        return 0

    if args.command == "delete":
        require_write_consent(args.store, args.consent)
        if not args.key:
            raise SystemExit("No keys provided. Use --key dot.path")
        deleted = 0
        for key in args.key:
            if del_nested(payload, key):
                deleted += 1
        payload["updated_at"] = now_iso()
        write_json(path, payload)
        print(json.dumps({"status": "ok", "file": str(path), "deleted": deleted}, ensure_ascii=False, indent=2))
        return 0

    if args.command == "reset":
        if args.confirm != "YES":
            raise SystemExit("Refusing reset. Pass --confirm YES")
        reset_payload = deepcopy(default)
        if "updated_at" in reset_payload:
            reset_payload["updated_at"] = now_iso()
        write_json(path, reset_payload)
        print(json.dumps({"status": "ok", "file": str(path), "reset": True}, ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
