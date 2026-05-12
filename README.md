<div align="center">

<p><strong>English</strong> | <a href="README.zh-CN.md">简体中文</a></p>

# You Are Not Alone

<h3>Safety-first mental-care support for AI assistants — now with OpenClaw bot access.</h3>

<p>
  Give distressed users one calm next step, route crisis signals first, prepare care conversations, plan gentle outings, clarify career pressure, and keep sensitive notes local.
</p>

<p>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <img alt="Version" src="https://img.shields.io/badge/version-2.0.0-black.svg">
  <img alt="OpenClaw" src="https://img.shields.io/badge/OpenClaw-bot%20gateway-ff6b35.svg">
  <img alt="Safety first" src="https://img.shields.io/badge/safety--first-crisis--aware-blue.svg">
  <img alt="Local first" src="https://img.shields.io/badge/local--first-privacy--minded-5f4bb6.svg">
</p>

<p>
  <a href="#openclaw-first">OpenClaw First</a> ·
  <a href="#why-teams-use-it">Why Teams Use It</a> ·
  <a href="#visual-demo">Visual Demo</a> ·
  <a href="#install">Install</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#what-it-does">What It Does</a> ·
  <a href="#local-data-and-privacy">Privacy</a> ·
  <a href="#safety-boundary">Safety</a>
</p>

</div>

---

## OpenClaw First

> **New in 2.0.0:** connect Feishu/Lark, Discord, Telegram, Slack, WhatsApp, Teams, and other OpenClaw channel bots as dedicated mental-care entry points in one command.

```bash
bash scripts/install_openclaw.sh --channel telegram --bot-id mental-care-telegram --consent true
```

What this unlocks:

- **Meet users where they already talk** — route supported OpenClaw channel bots into the same safety-first workflow.
- **Designate a dedicated care specialist** — mark one existing bot as the mental-care specialist with `scripts/configure_openclaw_bot.py`.
- **Keep secrets out of the skill** — local storage only keeps non-secret routing metadata; bot tokens and model keys stay in OpenClaw or provider secret stores.
- **Stay local-first** — mental-health logs remain separated from channel metadata and require explicit consent before writing.

---

## Why Teams Use It

`mental-care-skill` is a mental-health support skill, not a diagnosis or treatment tool. Current repository version: `2.0.0` (also recorded in `VERSION`).

The product promise is simple: when someone feels overwhelmed, they should not have to choose the right mode or explain everything perfectly. The assistant quietly checks safety first, keeps the first step small, and then opens optional paths only when appropriate.

| Product outcome | User-facing value |
| :--- | :--- |
| **Less cognitive load** | Short, warm responses with one doable default step. |
| **Safer routing** | Crisis, self-harm, overdose, severe confusion, and immediate danger signals are handled before optional modules. |
| **Practical follow-through** | Draft notes for doctors, therapists, school support, workplace support, trusted people, or emergency care. |
| **Private continuity** | Optional local records for trends and follow-up, with consent checks and no default raw transcript storage. |
| **Omnichannel access** | OpenClaw bots can become mental-care entry points without moving sensitive records into chat channels. |

> [!IMPORTANT]
> This project is not a diagnosis tool, not a therapist, and not a replacement for emergency or professional care. If you or someone else may be in immediate danger, contact local emergency services, a crisis line, or a trusted person nearby.

---

## Visual Demo

Use the skill from VS Code/Codex by asking for `$mental-care-skill`; the assistant loads the safety-first workflow, keeps the first response small, and only writes local records after explicit consent.

![VS Code demo showing the skill prompt, references, scripts, and assistant preview](docs/assets/vscode-demo.svg)

The diagrams below show the product at a glance: the architecture map explains how references, scripts, and isolated local stores fit together; the safety-routing chart shows why crisis and urgent-care logic always runs before optional outing or career modules.

<p align="center">
  <img src="docs/assets/architecture-map.svg" alt="Architecture map for safety routing, references, scripts, and isolated data stores" width="49%">
  <img src="docs/assets/safety-routing.svg" alt="Safety routing flowchart from user message to crisis, urgent, care, or self-help support" width="49%">
</p>

---

## Install

Install for Codex plus mainstream AI IDE bridge files (VS Code/Copilot, Cursor, Trae/Tare, and AGENTS.md):

```bash
bash scripts/install.sh --ide all --target "$PWD"
```

One-command download + install from a Git URL (replace the URL with your fork or published repository):

```bash
MENTAL_CARE_REPO_URL="https://github.com/<owner>/mental-care-skill.git" bash -c 'tmp="$(mktemp -d)"; git clone --depth 1 "$MENTAL_CARE_REPO_URL" "$tmp"; bash "$tmp/scripts/install.sh" --ide all --target "$PWD"; rm -rf "$tmp"'
```

Only install selected IDE integrations:

```bash
bash scripts/install.sh --ide vscode,cursor --target "$PWD"
bash scripts/install.sh --ide trae --skip-codex --target "$PWD"
```

---

## Quick Start

Use the skill directly:

```text
Use $mental-care-skill to provide safety-first mental-health support, then optionally guide low-burden outing or career clarification when appropriate, and save only consented local records.
```

Use the web fallback:

```text
Please follow the uploaded You Are Not Alone Web Prompt. Start with a low-burden check-in and do not ask me to choose a module.
```

Initialize and validate the local data store:

```bash
python scripts/init_local_data.py
python scripts/validate_local_data.py
```

Append one consented event entry:

```bash
python scripts/append_event_log.py --field save_consent=true --field session_type=checkin --field mood_score=4 --field anxiety_score=6 --field energy_score=3
```

Summarize recent trends without diagnosis:

```bash
python scripts/summarize_trends.py
```

---

## OpenClaw Bot Install

OpenClaw acts as the chat-channel gateway while `mental-care-skill` remains the safety policy. The project includes code-driven setup for Feishu/Lark, Discord, Telegram, Slack, WhatsApp, Teams, and other OpenClaw-supported channel bots.

Install the bridge and designate a bot as the dedicated mental-care specialist:

```bash
bash scripts/install_openclaw.sh --channel telegram --bot-id mental-care-telegram --consent true
```

Run OpenClaw gateway installation and onboarding from the same command:

```bash
bash scripts/install_openclaw.sh --install-gateway --onboard --channel feishu --bot-id feishu-care --consent true
```

Designate or update a specific existing OpenClaw bot without reinstalling the bridge:

```bash
python scripts/configure_openclaw_bot.py set \
  --bot-id mental-care-discord \
  --channel discord \
  --display-name "Mental Care" \
  --allowed-user-ids '["123456"]' \
  --consent true
```

The local database file is `~/mental_care_data/openclaw_dedicated_bots.json`. It stores only non-secret routing metadata; keep bot tokens, provider API keys, and channel secrets in OpenClaw or provider secret stores.

---

## What It Does

| Area | What the skill supports |
| :--- | :--- |
| **First response** | Gentle, short replies for low mood, anxiety, shame, loneliness, or overwhelm. |
| **Stabilization** | Grounding, tiny next steps, worry containment, and low-friction evening check-ins. |
| **Crisis-aware routing** | Self-harm, suicidal thoughts, overdose, harm to others, severe confusion, and unsafe situations. |
| **Care preparation** | Notes for doctors, therapists, school services, workplace support, urgent care, or emergency care. |
| **Local memory** | Optional consented logs for mood records, daily summaries, support contacts, and trend summaries. |
| **OpenClaw Bot (2.0.0)** | One-command bridge install for OpenClaw channel bots and local designation of a dedicated mental-care specialist. |
| **Gentle Outing Planner (2.0.0)** | Nearby short outings, city micro-trips, and condition-gated cross-city or overnight plans. |
| **Roundtrip Export (2.0.0)** | POI-rich itinerary export for copy, screenshot, OCR, and local HTML import. |
| **Career Compass (2.0.0)** | Low-burden career-direction clarification tied to current emotional load. |
| **Job Market Browser (2.0.0)** | Browser-based job-post collection with explicit consent checkpoints. |
| **Local Code Career Profile (2.0.0)** | Evidence-based skill profiling from user-authorized local projects only. |
| **Web fallback** | A standalone prompt for browser-based LLMs when the local skill is unavailable. |

---

## Demos

### Demo 1: Core low-burden support

```text
User: I have been anxious for days and I don't know whether I should see someone.
Assistant: That sounds exhausting. I cannot diagnose this, but several days of anxiety is worth bringing to a professional. If you want, I can help make a short care note: how long it has lasted, what changed in sleep/appetite, how it affects your day, and what you want to ask.
```

### Demo 2: OpenClaw specialist bot

```bash
bash scripts/install_openclaw.sh --channel discord --bot-id team-care-bot --consent true
python scripts/configure_openclaw_bot.py list
```

### Demo 3: Gentle outing planning

```text
User: I feel trapped at home and my head is too full.
Assistant: You do not need to solve everything right now. Let's make one low-burden environment shift: a 40-minute route with one open-air point, one sit-down point, and an easy return option.
```

### Demo 4: Career clarification + job fit

```text
User: I feel stuck professionally, but job searching makes me panic.
Assistant: Let's keep this low-pressure. We can do two tracks: identify what your current projects already prove, or compare one small set of real job posts. You only need to choose one first step.
```

### Demo 5: Roundtrip export flow

```bash
python scripts/export_roundtrip_itinerary.py --itinerary itinerary.json
python scripts/validate_itinerary_export.py --itinerary itinerary.json --export-dir ~/mental_care_data/exports/roundtrip/2026-04-25-example
```

---

## Confidence, Audit, and Hardening

No mental-health support tool should claim literal 100% certainty. This repository is designed to make confidence factual instead of absolute: safety boundaries are explicit, local writes are consent-gated, tests cover key privacy behaviors, and scripts can be re-validated after changes.

Recommended release loop:

1. Inspect architecture, prompts, scripts, and data boundaries.
2. Run tests and syntax checks.
3. Validate the local data directory.
4. Test OpenClaw bridge installation in a temporary directory.
5. Patch the smallest credible fix for any issue, then repeat until current evidence supports release.

Recent hardening focus areas:

- CSV log values are escaped before writing so spreadsheet apps do not execute user-provided formulas when logs are opened manually.
- Profile-store updates and deletions require explicit write consent through `scripts/manage_profile_data.py`.
- Date-scoped deletions reject malformed or inverted date ranges before touching local files.
- OpenClaw bot routing stores only non-secret metadata and requires explicit consent for set/delete operations.

---

## Web Prompt

If local scripting is unavailable, use the standalone browser prompt:

- Prompt file: [网页版/mental-care-web-prompt.md](网页版/mental-care-web-prompt.md)

The web prompt is designed for browser-based LLM usage and avoids pretending it can write local files.

---

## Local Data and Privacy

Default local path:

```text
~/mental_care_data/
```

| Domain | Files |
|---|---|
| Mental-health logs | `event_log.csv`, `daily_summary.csv`, `support_contacts.csv` |
| 2.0.0 outing/career/job/OpenClaw stores | `outing_preferences.json`, `career_profile.json`, `job_posts_cache.json`, `openclaw_dedicated_bots.json`, `exports/roundtrip/` |

Privacy defaults:

- Save minimal structured summaries, not raw conversation text by default.
- Ask for consent before saving each record type unless ongoing consent is explicitly configured.
- Validate local mood/function scores, dates, and known fields before writing records.
- Escape CSV cells that could be interpreted as formulas when opened in spreadsheet software.
- Let users inspect, summarize, update, validate, dry-run deletion, or delete records.
- Keep mental-health records isolated from external websites, job platforms, career data, and OpenClaw channel metadata unless the user explicitly consents.
- Require explicit consent before saving browser-collected job posts, normalized job caches, or profile-store updates/deletions.
- Do not store absolute local code paths in career profiles unless `--include-path` is explicitly used.

---

## Safety Boundary

This project deliberately avoids clinical overreach.

- Do not diagnose mental disorders.
- Do not replace therapy, medical care, emergency services, or crisis lines.
- Do not advise starting, stopping, increasing, decreasing, or substituting medication.
- Do not provide self-harm methods, lethal means, concealment advice, or detailed harmful plans.
- Do not save local records without consent.
- Do not send mental-health records to external services without explicit consent.
- Do not auto-apply jobs, auto-contact recruiters, or auto-submit personal information.

---

## Repository Layout

<details open>
<summary><strong>View Repository Tree</strong></summary>

```text
mental-care-skill/
├── README.md
├── README.zh-CN.md
├── VERSION
├── SKILL.md
├── docs/assets/
│   ├── vscode-demo.svg
│   ├── architecture-map.svg
│   └── safety-routing.svg
├── references/
│   ├── openclaw-integration.md
│   ├── triage-router.md
│   ├── crisis-protocol.md
│   └── ...
├── scripts/
│   ├── install.sh
│   ├── install_openclaw.sh
│   ├── configure_openclaw_bot.py
│   ├── init_local_data.py
│   ├── validate_local_data.py
│   └── ...
├── tests/
└── 网页版/
```

</details>

---

## Suggested GitHub Topics

```text
mental-health
mental-health-chatbot
openclaw
llm
ai-companion
crisis-support
suicide-prevention
anxiety
depression
self-help
prompt-engineering
local-first
privacy
career-guidance
travel-planning
```

---

## License

MIT License. See [LICENSE](LICENSE).
