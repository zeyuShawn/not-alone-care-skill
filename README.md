# You Are Not Alone

<p align="center">
  <strong>Safety-first mental-health support with low-burden routing, crisis navigation, optional outing recovery, and career-direction clarification.</strong>
</p>

`not-alone-care-skill` is a mental-health support skill, not a diagnosis or treatment tool.

Core principle: the user should not carry extra cognitive load when distressed. The assistant routes risk first, gives a default low-burden step, and only then introduces optional modules when safe.

## What ver2 adds

- `Gentle Outing Planner`: nearby short outing, city micro-trip, and condition-gated cross-city/overnight planning.
- `Roundtrip Export`: POI-rich exports for copy, screenshot, OCR, and local HTML import.
- `Career Compass`: low-burden career-direction clarification.
- `Job Market Browser`: browser-based job-post collection with consent checkpoints.
- `Local Code Career Profile`: evidence-based skill profile from user-authorized local projects.
- Data isolation with independent JSON files (`outing_preferences.json`, `career_profile.json`, `job_posts_cache.json`) separated from mental-health CSV logs.

## Safety boundary

- Must not diagnose.
- Must not replace professional or emergency care.
- Must prioritize crisis safety over all normal planning.
- Must not share mental-health records with external services without consent.
- Must not auto-apply jobs, auto-contact recruiters, or auto-submit personal information.

## Repository layout

```text
not-alone-care-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── triage-router.md
│   ├── crisis-protocol.md
│   ├── crisis-resources.md
│   ├── self-help-modules.md
│   ├── care-navigation.md
│   ├── support-network.md
│   ├── tone-controller.md
│   ├── stable-companion.md
│   ├── evening-checkin.md
│   ├── privacy-and-consent.md
│   ├── long-term-memory.md
│   ├── localization.md
│   ├── outing-planner.md
│   ├── outing-roundtrip-export.md
│   ├── career-compass.md
│   ├── job-market-browser.md
│   ├── local-code-career-profile.md
│   └── external-data-privacy.md
├── scripts/
│   ├── _local_data.py
│   ├── init_local_data.py
│   ├── append_event_log.py
│   ├── append_daily_summary.py
│   ├── manage_support_contacts.py
│   ├── summarize_trends.py
│   ├── delete_log_entries.py
│   ├── export_roundtrip_itinerary.py
│   ├── validate_itinerary_export.py
│   ├── collect_job_posts_browser.py
│   ├── normalize_job_posts.py
│   ├── analyze_local_code_profile.py
│   ├── rank_job_fit.py
│   └── manage_profile_data.py
└── 网页版/
    └── not-alone-care-web-prompt.md
```

## Local data

Default path:

```text
~/not_alone_care_data/
```

Mental-health logs:

- `event_log.csv`
- `daily_summary.csv`
- `support_contacts.csv`

ver2 JSON data:

- `outing_preferences.json`
- `career_profile.json`
- `job_posts_cache.json`
- `exports/roundtrip/`

## Quick start

Initialize local data:

```bash
python scripts/init_local_data.py
```

Append one consented event record:

```bash
python scripts/append_event_log.py --field save_consent=true --field session_type=checkin --field mood_score=4
```

Export itinerary assets:

```bash
python scripts/export_roundtrip_itinerary.py --itinerary itinerary.json
```

Validate itinerary export:

```bash
python scripts/validate_itinerary_export.py --itinerary itinerary.json --export-dir ~/not_alone_care_data/exports/roundtrip/2026-04-25-example
```

Normalize job posts:

```bash
python scripts/normalize_job_posts.py --input raw_posts.json --output normalized_posts.json
```

Analyze authorized local projects:

```bash
python scripts/analyze_local_code_profile.py --consent true --project repo1=~/work/project-a --target-role "Data Engineer"
```

Rank job fit:

```bash
python scripts/rank_job_fit.py --profile ~/not_alone_care_data/career_profile.json --posts ~/not_alone_care_data/job_posts_cache.json
```

## License

MIT License. See `LICENSE`.
