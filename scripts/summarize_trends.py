from __future__ import annotations

import argparse
import json
from statistics import mean

from _local_data import ensure_data_dir, numeric, read_rows


def average(rows: list[dict[str, str]], field: str) -> float | None:
    values = [numeric(row.get(field, "")) for row in rows]
    values = [value for value in values if value is not None]
    return round(mean(values), 2) if values else None


def collect_warnings(events: list[dict[str, str]], daily: list[dict[str, str]]) -> list[str]:
    warnings: list[str] = []
    recent_events = events[-10:]
    recent_daily = daily[-7:]

    if any(row.get("risk_level", "").lower() in {"orange", "red"} for row in recent_events):
        warnings.append("Recent records include elevated risk signals; consider real-world support.")
    if any("self" in row.get("warning_signals", "").lower() or "自伤" in row.get("warning_signals", "") for row in recent_daily):
        warnings.append("Recent daily summaries mention self-harm-related warning signals.")

    mood = average(recent_daily, "mood_avg")
    anxiety = average(recent_daily, "anxiety_avg")
    energy = average(recent_daily, "energy_avg")
    function = average(recent_daily, "function_score")

    if mood is not None and mood <= 3:
        warnings.append("Average mood is low in recent daily summaries.")
    if anxiety is not None and anxiety >= 7:
        warnings.append("Average anxiety is high in recent daily summaries.")
    if energy is not None and energy <= 3:
        warnings.append("Average energy is low in recent daily summaries.")
    if function is not None and function <= 3:
        warnings.append("Function score is low in recent daily summaries.")

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize local mental-health trends without diagnosis.")
    parser.add_argument("--data-dir", default=None)
    args = parser.parse_args()

    root = ensure_data_dir(args.data_dir)
    events = read_rows(root / "event_log.csv")
    daily = read_rows(root / "daily_summary.csv")

    recent_daily = daily[-7:]
    summary = {
        "data_dir": str(root),
        "event_count": len(events),
        "daily_count": len(daily),
        "recent_7_day_averages": {
            "mood_avg": average(recent_daily, "mood_avg"),
            "anxiety_avg": average(recent_daily, "anxiety_avg"),
            "energy_avg": average(recent_daily, "energy_avg"),
            "sleep_hours": average(recent_daily, "sleep_hours"),
            "function_score": average(recent_daily, "function_score"),
        },
        "warnings": collect_warnings(events, daily),
        "note": "This is a trend summary, not a diagnosis.",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
