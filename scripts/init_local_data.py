from __future__ import annotations

import argparse
import json

from _local_data import ensure_data_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize local not-alone-care CSV data.")
    parser.add_argument("--data-dir", default=None, help="Target data directory. Defaults to ~/not_alone_care_data.")
    args = parser.parse_args()

    root = ensure_data_dir(args.data_dir)
    print(json.dumps({"data_dir": str(root), "status": "ok"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
