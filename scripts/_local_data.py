from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

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


def default_data_dir() -> Path:
    return Path.home() / "not_alone_care_data"


def resolve_data_dir(data_dir: str | None) -> Path:
    return Path(data_dir).expanduser().resolve() if data_dir else default_data_dir()


def now_parts() -> tuple[str, str]:
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "是", "同意", "可以"}


def ensure_csv(path: Path, fields: Iterable[str]) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding=ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=list(fields))
        writer.writeheader()


def ensure_data_dir(data_dir: str | None = None) -> Path:
    root = resolve_data_dir(data_dir)
    root.mkdir(parents=True, exist_ok=True)
    ensure_csv(root / "event_log.csv", EVENT_FIELDS)
    ensure_csv(root / "daily_summary.csv", DAILY_FIELDS)
    ensure_csv(root / "support_contacts.csv", CONTACT_FIELDS)
    settings = root / "settings.json"
    if not settings.exists():
        settings.write_text(
            json.dumps(DEFAULT_SETTINGS, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return root


def parse_fields(items: List[str]) -> Dict[str, str]:
    row: Dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Expected key=value, got: {item}")
        key, value = item.split("=", 1)
        row[key.strip()] = value.strip()
    return row


def append_row(path: Path, fields: List[str], row: Dict[str, object]) -> None:
    clean = {field: str(row.get(field, "") or "") for field in fields}
    with path.open("a", newline="", encoding=ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(clean)


def read_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding=ENCODING) as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, fields: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", newline="", encoding=ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def numeric(value: str) -> float | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except ValueError:
        return None
