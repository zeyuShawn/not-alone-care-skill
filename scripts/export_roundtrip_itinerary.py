from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path
from typing import Any, Dict, List

from _local_data import ensure_data_dir, ensure_roundtrip_export_dir

SENSITIVE_TERMS = [
    "自伤",
    "自杀",
    "轻生",
    "suicide",
    "self-harm",
    "overdose",
    "抑郁",
    "焦虑",
    "panic",
    "危机",
]

GENERIC_POI_PATTERNS = [
    r"^附近[\u4e00-\u9fa5A-Za-z]+$",
    r"^一个[\u4e00-\u9fa5A-Za-z]+$",
    r"^某[\u4e00-\u9fa5A-Za-z]+$",
    r"^park$",
    r"^cafe$",
]

ADDRESS_PATTERNS = [
    r"\d{6}",
    r"\b\d{11}\b",
    r"\b\d{2,3}-\d{7,8}\b",
    r"\d+\.\d{5,}\s*,\s*\d+\.\d{5,}",
]


def _load_yaml(path: Path, text: str) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit("YAML input requires PyYAML. Please install pyyaml or provide JSON.") from exc
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise SystemExit("Itinerary root must be an object.")
    return data


def load_itinerary(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return _load_yaml(path, text)
    data = json.loads(text)
    if not isinstance(data, dict):
        raise SystemExit("Itinerary root must be an object.")
    return data


def normalize_bool(value: Any) -> str:
    if isinstance(value, bool):
        return "必选" if value else "可选"
    s = str(value or "").strip().lower()
    if s in {"1", "true", "yes", "y", "must", "required", "必选"}:
        return "必选"
    if s in {"0", "false", "no", "n", "optional", "可选"}:
        return "可选"
    return "可选"


def scrub_text(value: str) -> str:
    text = str(value or "")
    for term in SENSITIVE_TERMS:
        text = re.sub(term, "[敏感信息已移除]", text, flags=re.IGNORECASE)
    for pattern in ADDRESS_PATTERNS:
        text = re.sub(pattern, "[敏感定位已移除]", text)
    return text.strip()


def is_generic_poi(name: str) -> bool:
    stripped = (name or "").strip()
    if not stripped:
        return True
    for pattern in GENERIC_POI_PATTERNS:
        if re.match(pattern, stripped, flags=re.IGNORECASE):
            return True
    generic_words = {"附近公园", "一个咖啡馆", "某商场", "某书店", "park", "cafe"}
    return stripped.lower() in generic_words


def normalize_itinerary(raw: Dict[str, Any]) -> Dict[str, Any]:
    route_name = raw.get("route_name") or raw.get("name") or raw.get("title") or "未命名路线"
    city = raw.get("city") or ""
    district = raw.get("district") or raw.get("area") or ""
    city_area = raw.get("city_area") or " ".join([part for part in [city, district] if part]).strip() or "待核验"

    pois_raw = raw.get("pois") or raw.get("itinerary") or raw.get("items") or []
    if not isinstance(pois_raw, list):
        raise SystemExit("POIs must be a list under `pois` or equivalent field.")

    pois: List[Dict[str, str]] = []
    warnings: List[str] = []
    for idx, poi_raw in enumerate(pois_raw, start=1):
        if not isinstance(poi_raw, dict):
            continue
        name = scrub_text(str(poi_raw.get("name") or poi_raw.get("title") or poi_raw.get("poi") or ""))
        ptype = scrub_text(str(poi_raw.get("type") or poi_raw.get("category") or "待核验"))
        stay = str(poi_raw.get("stay_minutes") or poi_raw.get("stay") or poi_raw.get("duration") or "待核验").strip()
        if stay.isdigit():
            stay = f"{stay} 分钟"
        purpose = scrub_text(str(poi_raw.get("purpose") or poi_raw.get("role") or poi_raw.get("function") or "待核验"))
        required = normalize_bool(poi_raw.get("required") or poi_raw.get("must") or poi_raw.get("is_required"))

        if is_generic_poi(name):
            warnings.append(f"POI {idx} 名称可能过于泛化: {name or '[空]'}")

        pois.append(
            {
                "name": name or f"待核验POI{idx}",
                "type": ptype or "待核验",
                "stay": stay or "待核验",
                "purpose": purpose or "待核验",
                "required": required,
            }
        )

    normalized = {
        "route_name": scrub_text(str(route_name)),
        "city_area": scrub_text(str(city_area)),
        "route_type": scrub_text(str(raw.get("route_type") or raw.get("type") or "低负担路线")),
        "fit_reason": scrub_text(str(raw.get("fit_reason") or raw.get("suitable_reason") or raw.get("reason") or "待核验")),
        "minimum_version": scrub_text(
            str(raw.get("minimum_version") or raw.get("minimal_version") or raw.get("minimum_plan") or "仅完成前 1-2 个点也算完成")
        ),
        "retreat_point": scrub_text(str(raw.get("retreat_point") or raw.get("exit_point") or "任一补给点可结束返回")),
        "safety_point": scrub_text(str(raw.get("safety_point") or raw.get("safety_note") or "选择交通方便、可坐下、可避雨地点")),
        "pois": pois,
        "warnings": warnings,
    }
    return normalized


def render_copy_text(itinerary: Dict[str, Any]) -> str:
    lines = [
        f"路线名：{itinerary['route_name']}",
        f"城市/区域：{itinerary['city_area']}",
        f"路线类型：{itinerary['route_type']}",
        f"适合原因：{itinerary['fit_reason']}",
        "",
    ]
    for i, poi in enumerate(itinerary["pois"], start=1):
        lines.extend(
            [
                f"POI {i}：{poi['name']}",
                f"类型：{poi['type']}",
                f"建议停留：{poi['stay']}",
                f"作用：{poi['purpose']}",
                f"是否必选：{poi['required']}",
                "",
            ]
        )
    lines.extend(
        [
            f"最小版本：{itinerary['minimum_version']}",
            f"撤退点：{itinerary['retreat_point']}",
            f"安全点：{itinerary['safety_point']}",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def render_screenshot_text(itinerary: Dict[str, Any]) -> str:
    lines = [
        f"路线名: {itinerary['route_name']}",
        f"城市: {itinerary['city_area']}",
        f"类型: {itinerary['route_type']}",
        "",
    ]
    for i, poi in enumerate(itinerary["pois"], start=1):
        lines.append(f"POI{i} {poi['name']} - {poi['type']} - {poi['stay']} - {poi['required']}")
        lines.append(f"作用: {poi['purpose']}")
    lines.extend(
        [
            "",
            f"最小版本: {itinerary['minimum_version']}",
            f"撤退点: {itinerary['retreat_point']}",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def render_ocr_text(itinerary: Dict[str, Any]) -> str:
    lines = [
        f"路线名 {itinerary['route_name']}",
        f"城市区域 {itinerary['city_area']}",
        f"路线类型 {itinerary['route_type']}",
        "",
    ]
    for i, poi in enumerate(itinerary["pois"], start=1):
        lines.extend(
            [
                f"POI {i}",
                f"名称 {poi['name']}",
                f"类型 {poi['type']}",
                f"停留 {poi['stay']}",
                f"作用 {poi['purpose']}",
                f"必选 {poi['required']}",
                "",
            ]
        )
    lines.extend(
        [
            f"最小版本 {itinerary['minimum_version']}",
            f"撤退点 {itinerary['retreat_point']}",
            f"安全点 {itinerary['safety_point']}",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def render_markdown(itinerary: Dict[str, Any]) -> str:
    lines = [
        f"# {itinerary['route_name']}",
        "",
        f"- 城市/区域: {itinerary['city_area']}",
        f"- 路线类型: {itinerary['route_type']}",
        f"- 适合原因: {itinerary['fit_reason']}",
        "",
        "## POI",
        "",
    ]
    for i, poi in enumerate(itinerary["pois"], start=1):
        lines.extend(
            [
                f"### POI {i}: {poi['name']}",
                f"- 类型: {poi['type']}",
                f"- 建议停留: {poi['stay']}",
                f"- 作用: {poi['purpose']}",
                f"- 是否必选: {poi['required']}",
                "",
            ]
        )
    lines.extend(
        [
            "## 收尾",
            "",
            f"- 最小版本: {itinerary['minimum_version']}",
            f"- 撤退点: {itinerary['retreat_point']}",
            f"- 安全点: {itinerary['safety_point']}",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def render_html(itinerary: Dict[str, Any]) -> str:
    poi_rows = []
    for i, poi in enumerate(itinerary["pois"], start=1):
        poi_rows.append(
            "\n".join(
                [
                    f"<section class=\"poi\"><h2>POI {i}: {escape(poi['name'])}</h2>",
                    f"<p><strong>类型:</strong> {escape(poi['type'])}</p>",
                    f"<p><strong>建议停留:</strong> {escape(poi['stay'])}</p>",
                    f"<p><strong>作用:</strong> {escape(poi['purpose'])}</p>",
                    f"<p><strong>是否必选:</strong> {escape(poi['required'])}</p></section>",
                ]
            )
        )
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{escape(itinerary['route_name'])}</title>
  <style>
    body {{ font-family: Arial, \"TeX Gyre Heros\", sans-serif; line-height: 1.5; margin: 24px; }}
    h1, h2 {{ margin-bottom: 8px; }}
    .meta {{ background: #f6f8fa; padding: 12px; border-radius: 8px; }}
    .poi {{ border-top: 1px solid #ddd; margin-top: 12px; padding-top: 12px; }}
  </style>
</head>
<body>
  <h1>{escape(itinerary['route_name'])}</h1>
  <div class=\"meta\">
    <p><strong>城市/区域:</strong> {escape(itinerary['city_area'])}</p>
    <p><strong>路线类型:</strong> {escape(itinerary['route_type'])}</p>
    <p><strong>适合原因:</strong> {escape(itinerary['fit_reason'])}</p>
    <p><strong>最小版本:</strong> {escape(itinerary['minimum_version'])}</p>
    <p><strong>撤退点:</strong> {escape(itinerary['retreat_point'])}</p>
    <p><strong>安全点:</strong> {escape(itinerary['safety_point'])}</p>
  </div>
  {''.join(poi_rows)}
</body>
</html>
"""


def write_outputs(target_dir: Path, itinerary: Dict[str, Any]) -> Dict[str, str]:
    files = {
        "copy.txt": render_copy_text(itinerary),
        "screenshot.txt": render_screenshot_text(itinerary),
        "ocr.txt": render_ocr_text(itinerary),
        "itinerary.md": render_markdown(itinerary),
        "itinerary.html": render_html(itinerary),
    }
    out_paths: Dict[str, str] = {}
    for filename, content in files.items():
        path = target_dir / filename
        path.write_text(content, encoding="utf-8")
        out_paths[filename] = str(path)
    return out_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Export itinerary to roundtrip-friendly text/HTML assets.")
    parser.add_argument("--itinerary", required=True, help="Path to itinerary JSON/YAML.")
    parser.add_argument("--data-dir", default=None, help="Data root, defaults to ~/not_alone_care_data.")
    parser.add_argument("--output-dir", default=None, help="Optional explicit output directory.")
    parser.add_argument("--strict", action="store_true", help="Fail if POI names are too generic.")
    args = parser.parse_args()

    source_path = Path(args.itinerary).expanduser().resolve()
    if not source_path.exists():
        raise SystemExit(f"Itinerary file not found: {source_path}")

    raw = load_itinerary(source_path)
    itinerary = normalize_itinerary(raw)

    root = ensure_data_dir(args.data_dir)
    if args.output_dir:
        target_dir = Path(args.output_dir).expanduser().resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
    else:
        target_dir = ensure_roundtrip_export_dir(root, itinerary["route_name"])

    if args.strict and itinerary["warnings"]:
        raise SystemExit("Strict mode failed: " + "; ".join(itinerary["warnings"]))

    outputs = write_outputs(target_dir, itinerary)
    summary = {
        "status": "ok",
        "source": str(source_path),
        "output_dir": str(target_dir),
        "files": outputs,
        "poi_count": len(itinerary["pois"]),
        "warnings": itinerary["warnings"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
