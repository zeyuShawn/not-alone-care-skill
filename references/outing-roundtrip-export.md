# Outing Roundtrip Export

Use this module to export POI-rich itinerary content for 圆周旅记/圆周旅迹 style import.

Goal: maximize POI recognition and usability, not pretty prose.

## Export Shapes

Provide four output variants:

- Copy text (`copy.txt`): direct paste format.
- Screenshot-friendly (`screenshot.txt`): short lines, strong POI markers, low table usage.
- OCR-friendly (`ocr.txt`): large headers, one POI per line block, simple symbols.
- Link/HTML (`itinerary.html`): local publishable structure for app link import.

Also provide `itinerary.md` as a canonical markdown copy.

## Recommended Field Order

Avoid complex tables. Use stable labels:

- Route name
- City/area
- Route type
- POI blocks:
  - Name
  - Type
  - Suggested stay
  - Purpose
  - Required or optional

Required route-level sections:

- Why this route fits the current state.
- Minimum version.
- Retreat point.

## Export Safety Rules

- Remove mental-health-sensitive text from exports.
- Keep only itinerary-essential information.
- Block full address, contact info, exact private residence coordinates by default.
- If uncertain data exists, label as `待核验`.

## Script Responsibilities

### `scripts/export_roundtrip_itinerary.py`

- Input: structured itinerary JSON/YAML.
- Output files:
  - `copy.txt`
  - `screenshot.txt`
  - `ocr.txt`
  - `itinerary.md`
  - `itinerary.html`
- Save path:
  - `~/not_alone_care_data/exports/roundtrip/YYYY-MM-DD-路线名/`
- Must run sensitive-text scrubbing.
- Must reject overly generic POI names when strict mode is on.

### `scripts/validate_itinerary_export.py`

Check:

- At least 2-3 explicit POIs.
- Each POI has name/type/stay/purpose/required flag.
- Route includes minimum version and retreat point.
- No sensitive terms, precise address, contact detail, exact coordinate leaks.
- Screenshot/OCR files have short lines and no complex table blocks.

## Link and Image Strategy

- Phase 1: local HTML generation only.
- Public publishing is out of default scope.
- Screenshot/OCR mode outputs text layout only, not image generation.
