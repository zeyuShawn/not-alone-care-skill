# You Are Not Alone

<p align="center">
  <strong>A safety-first LLM skill for mental-health support, crisis-aware routing, evening check-ins, care preparation, and local recovery notes.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <img alt="Safety first" src="https://img.shields.io/badge/safety--first-crisis--aware-blue.svg">
  <img alt="Local first" src="https://img.shields.io/badge/local--first-privacy--minded-purple.svg">
  <img alt="LLM skill" src="https://img.shields.io/badge/LLM-skill-black.svg">
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> |
  <a href="#web-prompt">Web prompt</a> |
  <a href="#demo">Demo</a> |
  <a href="#privacy">Privacy</a> |
  <a href="#safety-boundary">Safety boundary</a>
</p>

---

`not-alone-care-skill` helps an AI assistant respond more carefully when a user reports depression, anxiety, panic, emotional distress, loss of function, loneliness, hopelessness, self-harm thoughts, suicidal ideation, medication concerns, or difficulty seeking care.

The project follows one practical rule: a distressed user should not have to choose the right mode. The assistant quietly checks for risk signals, keeps the response low-burden, and shifts toward self-help, care preparation, support-network drafting, or crisis navigation as needed.

> This project is not a diagnosis tool, not a therapist, and not a replacement for emergency or professional care. If you or someone else may be in immediate danger, contact local emergency services, a crisis line, or a trusted person nearby.

## What it does

| Area | What the skill supports |
|---|---|
| First response | Gentle, short replies for low mood, anxiety, shame, loneliness, or overwhelm. |
| Stabilization | Grounding, tiny next steps, worry containment, and low-friction evening check-ins. |
| Crisis-aware routing | Self-harm, suicidal thoughts, overdose, harm to others, severe confusion, and unsafe situations. |
| Care preparation | Notes for doctors, therapists, school services, workplace support, urgent care, or emergency care. |
| Local memory | Optional CSV logs for consented mood records, daily summaries, support contacts, and trend summaries. |
| Web fallback | A standalone prompt for browser-based LLMs when the local skill is unavailable. |

## Web prompt

Some users will not have their computer or local skill environment nearby. For that case, this repository includes a single-file web prompt that can be uploaded to a browser-based LLM.

- Web prompt document: [网页版/not-alone-care-web-prompt.md](https://github.com/zeyuShawn/not-alone-care-skill/blob/main/%E7%BD%91%E9%A1%B5%E7%89%88/not-alone-care-web-prompt.md)
- Raw file for direct copy/download: [raw not-alone-care-web-prompt.md](https://raw.githubusercontent.com/zeyuShawn/not-alone-care-skill/main/%E7%BD%91%E9%A1%B5%E7%89%88/not-alone-care-web-prompt.md)

The web prompt removes local script dependencies. It asks the model to generate copyable summaries instead of pretending it can write local files.

## Quick start

Use the skill directly:

```text
Use $not-alone-care-skill to provide a gentle mental-health check-in, route risk safely, and save only consented local records.
```

Use the web fallback:

```text
Please follow the uploaded You Are Not Alone Web Prompt. Start with a low-burden check-in and do not ask me to choose a module.
```

Initialize local CSV files:

```bash
python scripts/init_local_data.py
```

Append a consented event entry:

```bash
python scripts/append_event_log.py --field save_consent=true --field session_type=checkin --field mood_score=4 --field anxiety_score=6 --field energy_score=3
```

Summarize recent local trends without diagnosis:

```bash
python scripts/summarize_trends.py
```

## Demo

### Chinese demo

```text
User:
我今天什么都不想做，觉得自己很没用。

Assistant:
我听见了。你现在像是已经撑了很久，不需要马上把原因讲清楚。

我们先不处理全部问题，只做一个很小的动作：坐起来，喝一口水。如果这个也太难，你只回我一个词，比如“累”“空”“烦”，也可以。
```

### English demo

```text
User:
I have been anxious for days and I don't know whether I should see someone.

Assistant:
That sounds exhausting, especially if it has been going on for several days. I cannot diagnose what is happening, but this is a reasonable thing to bring to a professional.

If it helps, we can make a short note for a doctor or therapist: how long this has been going on, what sleep and appetite look like, whether it is affecting work or school, and what you want to ask.
```

For immediate danger, the assistant should stop ordinary coaching and move toward real-world help: emergency services, a crisis line, a nearby trusted person, urgent care, or an emergency department.

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

## Safety boundary

This project deliberately avoids medical overreach.

- It does not diagnose mental disorders.
- It does not replace therapy, medical care, emergency services, crisis lines, or trusted real-world support.
- It does not advise starting, stopping, increasing, decreasing, mixing, or replacing medication.
- It does not provide self-harm methods, lethal means, concealment advice, or detailed discussion of plans.
- It does not save local records without consent.

`references/crisis-resources.md` contains a small set of starter crisis-resource entries verified on 2026-04-21. Re-verify hotline numbers and chat links before use whenever browsing is available. If a region-specific resource is not verified, advise the local emergency number, nearest emergency department, a trusted person nearby, or a current official source.

## Local data scripts

The scripts write only to a user-controlled directory. By default:

```text
~/not_alone_care_data
```

Add a support contact after consent:

```bash
python scripts/manage_support_contacts.py add --field name_or_alias=friend --field relationship=friend --field contact_method=placeholder --field available_time=evening --field preferred_for=emotional_support --field consent_to_use=true
```

Append a consented daily summary:

```bash
python scripts/append_daily_summary.py --field save_consent=true --field mood_avg=4 --field anxiety_avg=6 --field energy_avg=3 --field next_checkin=tomorrow
```

Delete records by explicit user request:

```bash
python scripts/delete_log_entries.py --target event --date 2026-04-21
```

## Privacy

Mental-health records are sensitive even when stored locally.

- Do not commit `event_log.csv`, `daily_summary.csv`, `support_contacts.csv`, `settings.json`, or local data directories.
- Do not store raw conversation text by default.
- Ask before saving each event unless the user has explicitly configured ongoing consent.
- Let users skip, inspect, summarize, or delete records.
- If a computer is shared, local CSV files may still be visible to others.

The included `.gitignore` blocks common local record files, validation data, Python cache files, and old `cure_yourself_data/` directories.

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

MIT License. See [LICENSE](LICENSE).
