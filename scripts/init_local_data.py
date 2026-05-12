from __future__ import annotations

import argparse
import json

from _local_data import ensure_data_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize local mental-care data files.")
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Target data directory. Defaults to ~/mental_care_data.",
    )
    args = parser.parse_args()

    root = ensure_data_dir(args.data_dir)
    payload = {
        "data_dir": str(root),
        "status": "ok",
        "csv_files": [
            "event_log.csv",
            "daily_summary.csv",
            "support_contacts.csv",
        ],
        "json_files": [
            "settings.json",
            "outing_preferences.json",
            "career_profile.json",
            "job_posts_cache.json",
            "openclaw_dedicated_bots.json",
        ],
        "directories": [
            "exports/roundtrip",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
