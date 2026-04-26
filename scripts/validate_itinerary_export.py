from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

SENSITIVE_TERMS = [
    "自伤",
    "自杀",
    "轻生",
    "suicide",
    "self-harm",
    "抑郁",
    "焦虑",
]

ADDRESS_PATTERNS = [
    r"\d{11}",
    r"\d{6}",
    r"\d+\.\d{5,}\s*,\s*\d+\.\d{5,}",
    r"(路|街|道|号)\d+",
]


def _load_yaml(path: Path, text: str) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit("YAML input requires PyYAML. Please install pyyaml or provide JSON.") from exc
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise SystemExit("Itinerary root must be object.")
    return data


def load_structured(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return _load_yaml(path, text)
    data = json.loads(text)
    if not isinstance(data, dict):
        raise SystemExit("Itinerary root must be object.")
    return data


def get_pois(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw = data.get("pois") or data.get("itinerary") or data.get("items") or []
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    return []


def find_sensitive_text(text: str) -> List[str]:
    found = []
    lower = text.lower()
    for term in SENSITIVE_TERMS:
        if term.lower() in lower:
            found.append(term)
    return sorted(set(found))


def find_precise_patterns(text: str) -> List[str]:
    hits: List[str] = []
    for pattern in ADDRESS_PATTERNS:
        if re.search(pattern, text):
            hits.append(pattern)
    return hits


def check_poi_completeness(pois: List[Dict[str, Any]]) -> List[str]:
    issues: List[str] = []

    def first_present(poi: Dict[str, Any], keys: List[str]) -> Any:
        for key in keys:
            if key not in poi:
                continue
            value = poi[key]
            if value is None:
                continue
            if isinstance(value, str) and value.strip() == "":
                continue
            return value
        return None

    for idx, poi in enumerate(pois, start=1):
        required = {
            "name": first_present(poi, ["name", "title", "poi"]),
            "type": first_present(poi, ["type", "category"]),
            "stay": first_present(poi, ["stay", "stay_minutes", "duration"]),
            "purpose": first_present(poi, ["purpose", "role", "function"]),
            "required": first_present(poi, ["required", "must", "is_required"]),
        }
        missing = [key for key, value in required.items() if value in (None, "")]
        if missing:
            issues.append(f"POI {idx} 缺少字段: {', '.join(missing)}")
    return issues


def check_route_fields(data: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    minimum = data.get("minimum_version") or data.get("minimal_version") or data.get("minimum_plan")
    retreat = data.get("retreat_point") or data.get("exit_point")
    if not minimum:
        issues.append("缺少最小版本字段 (minimum_version)")
    if not retreat:
        issues.append("缺少撤退点字段 (retreat_point)")
    return issues


def check_export_text_file(path: Path, short_line_limit: int = 90) -> Tuple[List[str], Dict[str, Any]]:
    issues: List[str] = []
    if not path.exists():
        return [f"文件不存在: {path.name}"], {"line_count": 0, "max_line_len": 0}

    lines = path.read_text(encoding="utf-8").splitlines()
    max_len = max((len(line) for line in lines), default=0)
    if max_len > short_line_limit:
        issues.append(f"{path.name} 存在过长行: {max_len} > {short_line_limit}")

    table_like = [line for line in lines if line.count("|") >= 3]
    if table_like:
        issues.append(f"{path.name} 疑似复杂表格行数量: {len(table_like)}")

    joined = "\n".join(lines)
    sensitive_hits = find_sensitive_text(joined)
    if sensitive_hits:
        issues.append(f"{path.name} 命中心理敏感词: {', '.join(sensitive_hits)}")

    pattern_hits = find_precise_patterns(joined)
    if pattern_hits:
        issues.append(f"{path.name} 命中精确地址/定位模式: {', '.join(pattern_hits)}")

    meta = {
        "line_count": len(lines),
        "max_line_len": max_len,
    }
    return issues, meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate itinerary data and roundtrip export files.")
    parser.add_argument("--itinerary", help="Path to source itinerary JSON/YAML.")
    parser.add_argument("--export-dir", help="Directory containing copy/screenshot/ocr export files.")
    args = parser.parse_args()

    if not args.itinerary and not args.export_dir:
        raise SystemExit("Provide at least one of --itinerary or --export-dir.")

    report: Dict[str, Any] = {
        "status": "ok",
        "checks": [],
        "issues": [],
        "meta": {},
    }

    if args.itinerary:
        src = Path(args.itinerary).expanduser().resolve()
        if not src.exists():
            raise SystemExit(f"Itinerary not found: {src}")
        data = load_structured(src)
        pois = get_pois(data)

        if len(pois) < 2:
            report["issues"].append("POI 数量少于 2")
        elif len(pois) < 3:
            report["checks"].append("POI 数量为 2：可用但建议提升到 3")
        else:
            report["checks"].append(f"POI 数量检查通过: {len(pois)}")

        report["issues"].extend(check_poi_completeness(pois))
        report["issues"].extend(check_route_fields(data))

        raw_text = json.dumps(data, ensure_ascii=False)
        sensitive_hits = find_sensitive_text(raw_text)
        if sensitive_hits:
            report["issues"].append("源 itinerary 包含心理敏感词: " + ", ".join(sensitive_hits))

        precise_hits = find_precise_patterns(raw_text)
        if precise_hits:
            report["issues"].append("源 itinerary 可能包含精确定位: " + ", ".join(precise_hits))

    if args.export_dir:
        export_dir = Path(args.export_dir).expanduser().resolve()
        files_to_check = ["copy.txt", "screenshot.txt", "ocr.txt"]
        export_meta: Dict[str, Any] = {}
        for name in files_to_check:
            issues, meta = check_export_text_file(export_dir / name)
            export_meta[name] = meta
            report["issues"].extend(issues)
        report["meta"]["export_files"] = export_meta

    if report["issues"]:
        report["status"] = "failed"

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
