from __future__ import annotations

import argparse
import json
from copy import deepcopy
from typing import Any, Dict, List

from _local_data import ensure_data_dir, now_iso, read_json, truthy, write_json

STORE_FILENAME = "openclaw_dedicated_bots.json"
SUPPORTED_CHANNELS = {
    "discord",
    "feishu",
    "lark",
    "telegram",
    "slack",
    "whatsapp",
    "wechat",
    "teams",
    "matrix",
    "signal",
    "other",
}

DEFAULT_STORE: Dict[str, Any] = {
    "version": 1,
    "updated_at": "",
    "consent": False,
    "active_bot_id": "",
    "bots": [],
    "routing_policy": {
        "mental_care_only": True,
        "require_explicit_skill_activation": False,
        "keep_records_local": True,
        "share_records_with_openclaw_channels": False,
    },
    "notes": "Stores non-secret OpenClaw channel/bot routing metadata only. Keep bot tokens in OpenClaw or channel provider secret stores.",
}

MENTAL_CARE_SYSTEM_PROMPT = """Use $mental-care-skill for this bot. Provide safety-first, non-diagnostic mental-health support. Route crisis and urgent-risk messages before optional modules. Do not save local records unless the user explicitly consents to that exact record type. Do not transmit mental-health records to external services. Do not reveal or request bot tokens."""


def require_consent(consent: str) -> None:
    if not truthy(consent):
        raise SystemExit("Refusing to change OpenClaw mental-care bot routing without --consent true.")


def load_store(data_dir: str | None) -> tuple[Any, Dict[str, Any]]:
    root = ensure_data_dir(data_dir)
    path = root / STORE_FILENAME
    payload = read_json(path, DEFAULT_STORE)
    if not isinstance(payload, dict):
        payload = deepcopy(DEFAULT_STORE)
    payload.setdefault("version", 1)
    payload.setdefault("updated_at", "")
    payload.setdefault("consent", False)
    payload.setdefault("active_bot_id", "")
    payload.setdefault("bots", [])
    payload.setdefault("routing_policy", deepcopy(DEFAULT_STORE["routing_policy"]))
    payload.setdefault("notes", DEFAULT_STORE["notes"])
    return path, payload


def validate_channel(value: str) -> str:
    channel = value.strip().lower()
    if channel not in SUPPORTED_CHANNELS:
        raise SystemExit(f"Unsupported channel '{value}'. Use one of: {', '.join(sorted(SUPPORTED_CHANNELS))}")
    return channel


def parse_json_list(raw: str, field_name: str) -> List[str]:
    if not raw.strip():
        return []
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{field_name} must be a JSON array of strings") from exc
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise SystemExit(f"{field_name} must be a JSON array of strings")
    return value


def bot_record(args: argparse.Namespace) -> Dict[str, Any]:
    channel = validate_channel(args.channel)
    return {
        "bot_id": args.bot_id.strip(),
        "channel": channel,
        "display_name": args.display_name.strip() or args.bot_id.strip(),
        "mental_care_specialist": True,
        "scope": args.scope,
        "allowed_user_ids": parse_json_list(args.allowed_user_ids, "--allowed-user-ids"),
        "allowed_chat_ids": parse_json_list(args.allowed_chat_ids, "--allowed-chat-ids"),
        "openclaw_agent": args.openclaw_agent.strip(),
        "system_prompt": args.system_prompt.strip() or MENTAL_CARE_SYSTEM_PROMPT,
        "crisis_escalation_note": args.crisis_escalation_note.strip(),
        "created_or_updated_at": now_iso(),
    }


def upsert_bot(payload: Dict[str, Any], record: Dict[str, Any]) -> None:
    bots = [bot for bot in payload.get("bots", []) if isinstance(bot, dict)]
    bot_id = record["bot_id"]
    for index, current in enumerate(bots):
        if current.get("bot_id") == bot_id:
            bots[index] = {**current, **record}
            break
    else:
        bots.append(record)
    payload["bots"] = bots
    payload["active_bot_id"] = bot_id
    payload["consent"] = True
    payload["updated_at"] = now_iso()


def remove_bot(payload: Dict[str, Any], bot_id: str) -> bool:
    bots = [bot for bot in payload.get("bots", []) if isinstance(bot, dict)]
    kept = [bot for bot in bots if bot.get("bot_id") != bot_id]
    removed = len(kept) != len(bots)
    payload["bots"] = kept
    if payload.get("active_bot_id") == bot_id:
        payload["active_bot_id"] = kept[0].get("bot_id", "") if kept else ""
    payload["updated_at"] = now_iso()
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Configure a local OpenClaw bot as the dedicated mental-care specialist without storing secrets."
    )
    parser.add_argument("--data-dir", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create local data files, including OpenClaw bot routing store.")
    sub.add_parser("list", help="Show configured OpenClaw mental-care bots.")

    set_bot = sub.add_parser("set", help="Designate or update one OpenClaw bot as the mental-care specialist.")
    set_bot.add_argument("--bot-id", required=True, help="Non-secret OpenClaw/channel bot identifier.")
    set_bot.add_argument("--channel", required=True, help="feishu/lark, discord, telegram, slack, whatsapp, etc.")
    set_bot.add_argument("--display-name", default="")
    set_bot.add_argument("--scope", choices=["personal", "team", "workspace"], default="personal")
    set_bot.add_argument("--openclaw-agent", default="mental-care-skill")
    set_bot.add_argument("--allowed-user-ids", default="[]", help='JSON array. Example: ["12345"].')
    set_bot.add_argument("--allowed-chat-ids", default="[]", help='JSON array. Example: ["private:12345"].')
    set_bot.add_argument("--system-prompt", default="")
    set_bot.add_argument("--crisis-escalation-note", default="Contact local emergency services or crisis lines when immediate danger is present.")
    set_bot.add_argument("--consent", default="", help="Required as true/yes after explicit owner consent.")

    unset_bot = sub.add_parser("unset", help="Remove a dedicated mental-care bot designation.")
    unset_bot.add_argument("--bot-id", required=True)
    unset_bot.add_argument("--consent", default="", help="Required as true/yes after explicit owner consent.")

    args = parser.parse_args()
    path, payload = load_store(args.data_dir)

    if args.command == "init":
        write_json(path, payload)
        print(json.dumps({"status": "ok", "file": str(path)}, ensure_ascii=False, indent=2))
        return 0

    if args.command == "list":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.command == "set":
        require_consent(args.consent)
        record = bot_record(args)
        if not record["bot_id"]:
            raise SystemExit("--bot-id cannot be empty")
        upsert_bot(payload, record)
        write_json(path, payload)
        print(json.dumps({"status": "ok", "file": str(path), "active_bot_id": record["bot_id"]}, ensure_ascii=False, indent=2))
        return 0

    if args.command == "unset":
        require_consent(args.consent)
        removed = remove_bot(payload, args.bot_id.strip())
        write_json(path, payload)
        print(json.dumps({"status": "ok", "file": str(path), "removed": removed}, ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
