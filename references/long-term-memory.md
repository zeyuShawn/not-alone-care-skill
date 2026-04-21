# Long-Term Memory

Use local memory to support trends and continuity, not to store raw therapy transcripts.

## Files

Default directory:

```text
~/not_alone_care_data/
```

Files:

```text
event_log.csv
daily_summary.csv
support_contacts.csv
settings.json
```

## Record Types

### Event log

Use for each meaningful interaction or emotional event after consent.

Required fields:

```csv
date,time,session_type,mood_score,anxiety_score,energy_score,sleep_hours,function_score,main_trigger,dominant_emotion,body_signal,action_taken,risk_level,care_suggestion,save_consent
```

### Daily summary

Use for evening check-ins or end-of-day summaries after consent.

Required fields:

```csv
date,mood_avg,anxiety_avg,energy_avg,sleep_hours,function_score,main_patterns,warning_signals,helpful_actions,tomorrow_anchor,next_checkin,save_consent
```

## Minimal Data Rule

Save summaries and structured tags. Do not save full raw conversation unless the user explicitly asks and understands the privacy risk.

## Trend Summary Rules

Use `scripts/summarize_trends.py` for summaries.

Allowed:

- "Your mood score has been lower for several days."
- "Sleep and energy both look worse this week."
- "Self-harm signals appeared in recent records; consider contacting real-world support."

Not allowed:

- "You relapsed."
- "You have major depression."
- "This proves medication is needed."
- "You are getting worse because you did not do the tasks."

## Warning Signals

Flag gently when records show:

- Several days of low mood.
- Several days of high anxiety.
- Sleep sharply reduced or very irregular.
- Energy and function both low.
- Repeated self-harm or hopelessness tags.
- Increasing isolation.
- Medication confusion.

## Consent Script

Before saving:

> 我可以把这次整理成一条本地 CSV 记录，方便以后看趋势。不会保存完整聊天原文。可以保存吗？

If the user says no:

> 好，这次不记录。我们只处理现在的事。
