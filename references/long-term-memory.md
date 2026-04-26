# Long-Term Memory

Use local memory for continuity and trend support, not raw therapy transcript storage.

## Data Root

```text
~/not_alone_care_data/
```

## Record Domains

Mental-health CSV:

- `event_log.csv`
- `daily_summary.csv`
- `support_contacts.csv`

ver2 JSON (separate from mental-health logs):

- `outing_preferences.json`
- `career_profile.json`
- `job_posts_cache.json`
- `exports/roundtrip/`

## Event Log Fields

```csv
date,time,session_type,mood_score,anxiety_score,energy_score,sleep_hours,function_score,main_trigger,dominant_emotion,body_signal,action_taken,risk_level,care_suggestion,save_consent
```

## Daily Summary Fields

```csv
date,mood_avg,anxiety_avg,energy_avg,sleep_hours,function_score,main_patterns,warning_signals,helpful_actions,tomorrow_anchor,next_checkin,save_consent
```

## Minimal Data Rule

- Save trend tags and concise summaries.
- Skip precise address, private coordinates, or sensitive contact leakage.
- Keep job cache and itinerary export independently deletable.

## JSON Management Rule

All ver2 JSON stores must support:

- view,
- update,
- delete.

Only save `outing_preferences.json` or `career_profile.json` after consent.

## Trend Summary Guardrails

Allowed:

- "Recent mood/energy trends look lower."
- "Recent records show higher anxiety burden."

Not allowed:

- Diagnostic statements.
- Medication conclusions.
- Blaming language.

## Consent Prompt

> 我可以把这次整理成一条本地摘要记录，方便后续看趋势。不会保存完整聊天原文。可以吗？
