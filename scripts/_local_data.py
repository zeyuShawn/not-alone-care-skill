from __future__ import annotations

import csv
import json
import os
import re
import tempfile
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

ENCODING = "utf-8-sig"

EVENT_FIELDS = [
    "date",
    "time",
    "session_type",
    "mood_score",
    "anxiety_score",
    "energy_score",
    "sleep_hours",
    "function_score",
    "main_trigger",
    "dominant_emotion",
    "body_signal",
    "action_taken",
    "risk_level",
    "care_suggestion",
    "save_consent",
]

DAILY_FIELDS = [
    "date",
    "mood_avg",
    "anxiety_avg",
    "energy_avg",
    "sleep_hours",
    "function_score",
    "main_patterns",
    "warning_signals",
    "helpful_actions",
    "tomorrow_anchor",
    "next_checkin",
    "save_consent",
]

CONTACT_FIELDS = [
    "name_or_alias",
    "relationship",
    "contact_method",
    "available_time",
    "preferred_for",
    "notes",
    "consent_to_use",
]

DEFAULT_SETTINGS = {
    "preferred_language": "auto",
    "country_or_region": None,
    "evening_checkin_enabled": True,
    "checkin_time": "21:30",
    "save_raw_text": False,
    "crisis_resources_region": None,
}

OUTING_PREFERENCES_DEFAULT = {
    "version": 1,
    "updated_at": "",
    "consent": False,
    "preferred_outing_types": [],
    "avoid": [],
    "transport_preferences": [],
    "energy_defaults": {
        "low": "nearby_short_route",
        "medium": "city_micro_trip",
        "high": "half_day_or_more",
    },
    "location_granularity": "city_or_district_only",
    "notes_summary": "",
}

CAREER_PROFILE_DEFAULT = {
    "version": 1,
    "updated_at": "",
    "consent": False,
    "sources": [],
    "current_role": "",
    "target_roles": [],
    "skills_evidenced": [],
    "skills_to_verify": [],
    "project_evidence": [],
    "constraints": {
        "location": "",
        "salary_floor": "",
        "remote_preference": "",
        "energy_load_limit": "",
    },
    "avoid": [],
    "notes_summary": "",
}

JOB_POSTS_CACHE_DEFAULT = {
    "version": 1,
    "updated_at": "",
    "source": "browser",
    "query": "",
    "posts": [],
}

OPENCLAW_DEDICATED_BOTS_DEFAULT = {
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

_GENERIC_ROUTE_FALLBACK = "itinerary"

EVENT_SCORE_FIELDS = {"mood_score", "anxiety_score", "energy_score", "function_score"}
DAILY_SCORE_FIELDS = {"mood_avg", "anxiety_avg", "energy_avg", "function_score"}
RISK_LEVELS = {"", "green", "yellow", "orange", "red", "绿", "黄", "橙", "红"}



def default_data_dir() -> Path:
    return Path.home() / "mental_care_data"


def resolve_data_dir(data_dir: str | None) -> Path:
    return Path(data_dir).expanduser().resolve() if data_dir else default_data_dir()


def now_parts() -> tuple[str, str]:
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "是", "同意", "可以"}


def ensure_csv(path: Path, fields: Iterable[str]) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding=ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=list(fields))
        writer.writeheader()


def ensure_json(path: Path, default_value: Dict[str, Any]) -> None:
    if path.exists():
        return
    payload = deepcopy(default_value)
    if isinstance(payload, dict) and "updated_at" in payload and not payload["updated_at"]:
        payload["updated_at"] = now_iso()
    write_json(path, payload)


def ensure_data_dir(data_dir: str | None = None) -> Path:
    root = resolve_data_dir(data_dir)
    root.mkdir(parents=True, exist_ok=True)

    ensure_csv(root / "event_log.csv", EVENT_FIELDS)
    ensure_csv(root / "daily_summary.csv", DAILY_FIELDS)
    ensure_csv(root / "support_contacts.csv", CONTACT_FIELDS)

    settings = root / "settings.json"
    if not settings.exists():
        write_json(settings, DEFAULT_SETTINGS)

    ensure_json(root / "outing_preferences.json", OUTING_PREFERENCES_DEFAULT)
    ensure_json(root / "career_profile.json", CAREER_PROFILE_DEFAULT)
    ensure_json(root / "job_posts_cache.json", JOB_POSTS_CACHE_DEFAULT)
    ensure_json(root / "openclaw_dedicated_bots.json", OPENCLAW_DEDICATED_BOTS_DEFAULT)

    (root / "exports" / "roundtrip").mkdir(parents=True, exist_ok=True)
    return root


def parse_fields(items: List[str]) -> Dict[str, str]:
    row: Dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Expected key=value, got: {item}")
        key, value = item.split("=", 1)
        row[key.strip()] = value.strip()
    return row


def unknown_fields(fields: List[str], row: Dict[str, object]) -> List[str]:
    allowed = set(fields)
    return sorted(key for key in row.keys() if key not in allowed)


def validate_no_unknown_fields(fields: List[str], row: Dict[str, object]) -> None:
    extra = unknown_fields(fields, row)
    if extra:
        raise ValueError("Unknown field(s): " + ", ".join(extra))


def validate_date(value: str, field_name: str = "date") -> None:
    if not value:
        return
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format") from exc


def validate_time(value: str, field_name: str = "time") -> None:
    if not value:
        return
    try:
        datetime.strptime(value, "%H:%M:%S")
    except ValueError as exc:
        raise ValueError(f"{field_name} must use HH:MM:SS format") from exc


def escape_csv_cell(value: object) -> str:
    """Prevent spreadsheet formula execution when local CSV logs are opened manually."""
    text = str(value or "")
    if text and text[0] in {"=", "+", "-", "@", "\t", "\r"}:
        return "'" + text
    return text


def validate_range(row: Dict[str, object], field_names: Iterable[str], low: float, high: float) -> None:
    for field in field_names:
        raw = row.get(field, "")
        if raw is None or str(raw).strip() == "":
            continue
        value = numeric(str(raw))
        if value is None or value < low or value > high:
            raise ValueError(f"{field} must be a number from {low:g} to {high:g}")


def validate_sleep_hours(row: Dict[str, object]) -> None:
    raw = row.get("sleep_hours", "")
    if raw is None or str(raw).strip() == "":
        return
    value = numeric(str(raw))
    if value is None or value < 0 or value > 24:
        raise ValueError("sleep_hours must be a number from 0 to 24")


def validate_event_row(row: Dict[str, object]) -> None:
    validate_no_unknown_fields(EVENT_FIELDS, row)
    validate_date(str(row.get("date", "")))
    validate_time(str(row.get("time", "")))
    validate_range(row, EVENT_SCORE_FIELDS, 1, 10)
    validate_sleep_hours(row)
    risk = str(row.get("risk_level", "")).strip().lower()
    if risk not in RISK_LEVELS:
        raise ValueError("risk_level must be one of green/yellow/orange/red or blank")


def validate_daily_row(row: Dict[str, object]) -> None:
    validate_no_unknown_fields(DAILY_FIELDS, row)
    validate_date(str(row.get("date", "")))
    validate_range(row, DAILY_SCORE_FIELDS, 1, 10)
    validate_sleep_hours(row)


def atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=path.parent, encoding=encoding, newline="") as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def append_row(path: Path, fields: List[str], row: Dict[str, object]) -> None:
    validate_no_unknown_fields(fields, row)
    clean = {field: escape_csv_cell(row.get(field, "")) for field in fields}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="", encoding=ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(clean)


def read_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding=ENCODING) as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, fields: List[str], rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=path.parent, newline="", encoding=ENCODING) as tmp:
        writer = csv.DictWriter(tmp, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: escape_csv_cell(row.get(field, "")) for field in fields})
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def read_json(path: Path, default_value: Dict[str, Any] | None = None) -> Dict[str, Any]:
    if not path.exists():
        return deepcopy(default_value) if default_value is not None else {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def slugify_name(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return _GENERIC_ROUTE_FALLBACK
    value = re.sub(r"[\\/:*?\"<>|]", "-", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    value = value.strip("-._")
    return value or _GENERIC_ROUTE_FALLBACK


def ensure_roundtrip_export_dir(root: Path, route_name: str, date_str: str | None = None) -> Path:
    date_part = date_str or datetime.now().strftime("%Y-%m-%d")
    route_part = slugify_name(route_name)
    target = root / "exports" / "roundtrip" / f"{date_part}-{route_part}"
    target.mkdir(parents=True, exist_ok=True)
    return target


def numeric(value: str) -> float | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except ValueError:
        return None
