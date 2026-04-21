# You Are Not Alone

Safety-first LLM skill for low-burden mental-health support, crisis-aware routing, evening check-ins, care preparation, and optional local recovery notes.

This project is not a diagnosis tool, not a therapist, and not a replacement for emergency or professional care. If you or someone else may be in immediate danger, contact local emergency services, a crisis line, or a trusted person nearby.

## What this is

`not-alone-care-skill` is a modular skill for AI agents. It helps an assistant respond more carefully when a user reports depression, anxiety, panic, emotional distress, loss of function, loneliness, hopelessness, self-harm thoughts, suicidal ideation, medication concerns, or difficulty seeking care.

The skill is designed around one constraint: the user should not have to choose a mode while distressed. The assistant quietly checks for risk signals, responds in a low-burden way, and shifts toward self-help, care preparation, support-network drafting, or crisis navigation as needed.

## What it can help with

- Gentle first response for low mood, anxiety, shame, loneliness, or overwhelm.
- Grounding and tiny next steps for panic, rumination, avoidance, or low energy.
- Crisis-aware routing for self-harm, suicidal thoughts, overdose, harm to others, severe confusion, or unsafe situations.
- Care-preparation notes for doctors, therapists, school services, workplace support, or urgent care.
- Evening check-ins with minimal questions.
- Optional local CSV logs for consented mood records, daily summaries, support contacts, and trend summaries.
- A standalone web prompt for temporary use in browser-based LLMs when the local skill is unavailable.

## What it does not do

- It does not diagnose mental disorders.
- It does not replace therapy, medical care, emergency services, crisis lines, or trusted real-world support.
- It does not advise starting, stopping, increasing, decreasing, mixing, or replacing medication.
- It does not provide self-harm methods, lethal means, concealment advice, or detailed discussion of plans.
- It does not save local records without consent.

## Repository layout

```text
not-alone-care-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── triage-router.md
│   ├── crisis-protocol.md
│   ├── tone-controller.md
│   ├── stable-companion.md
│   ├── self-help-modules.md
│   ├── care-navigation.md
│   ├── long-term-memory.md
│   ├── evening-checkin.md
│   ├── support-network.md
│   ├── localization.md
│   ├── crisis-resources.md
│   └── privacy-and-consent.md
├── scripts/
│   ├── init_local_data.py
│   ├── append_event_log.py
│   ├── append_daily_summary.py
│   ├── manage_support_contacts.py
│   ├── summarize_trends.py
│   ├── delete_log_entries.py
│   └── _local_data.py
├── 网页版/
│   └── not-alone-care-web-prompt.md
├── 测试记录.md
└── 讨论过程.md
```

## Quick start

Use the skill directly from this repository:

```text
Use $not-alone-care-skill to provide a gentle mental-health check-in, route risk safely, and save only consented local records.
```

For browser-based LLMs, upload or paste:

```text
网页版/not-alone-care-web-prompt.md
```

That standalone prompt removes local script dependencies and asks the model to generate copyable summaries instead of pretending it can write local files.

## Local data scripts

The local scripts write only to a user-controlled directory. By default:

```text
~/not_alone_care_data
```

Initialize local CSV files:

```bash
python scripts/init_local_data.py
```

Append a consented event entry:

```bash
python scripts/append_event_log.py --field save_consent=true --field session_type=checkin --field mood_score=4 --field anxiety_score=6 --field energy_score=3
```

Append a consented daily summary:

```bash
python scripts/append_daily_summary.py --field save_consent=true --field mood_avg=4 --field anxiety_avg=6 --field energy_avg=3 --field next_checkin=tomorrow
```

Add a support contact after consent:

```bash
python scripts/manage_support_contacts.py add --field name_or_alias=friend --field relationship=friend --field contact_method=placeholder --field available_time=evening --field preferred_for=emotional_support --field consent_to_use=true
```

Summarize trends without diagnosis:

```bash
python scripts/summarize_trends.py
```

## Privacy notes

Mental-health records are sensitive even when stored locally.

- Do not commit `event_log.csv`, `daily_summary.csv`, `support_contacts.csv`, `settings.json`, or local data directories.
- Do not store raw conversation text by default.
- Ask before saving each event unless the user has explicitly configured ongoing consent.
- Let users skip, inspect, summarize, or delete records.
- If a computer is shared, local CSV files may still be visible to others.

The included `.gitignore` blocks common local record files and Python cache files.

## Crisis resources

`references/crisis-resources.md` contains a small set of starter crisis-resource entries that were verified on 2026-04-21. Re-verify numbers and chat links before use whenever browsing is available. If a region-specific resource is not verified, advise the local emergency number, nearest emergency department, a trusted person nearby, or a current official source.

## Safety testing

See `测试记录.md` for the first scenario test pass. Covered scenarios include low mood, persistent functional impairment, panic, suicidal thoughts without plan, explicit plan and means, medication concerns, evening check-in, and support-contact use.

## Suggested GitHub topics

```text
mental-health
mental-health-chatbot
llm
ai-companion
crisis-support
suicide-prevention
anxiety
depression
cbt
wellbeing
self-help
prompt-engineering
openai
local-first
privacy
```

## License

No license has been added yet. Add a license before inviting public reuse or contributions.
