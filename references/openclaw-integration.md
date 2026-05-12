# OpenClaw Integration

Use this reference when the user wants to run `mental-care-skill` through an OpenClaw channel bot such as Feishu/Lark, Discord, Telegram, Slack, WhatsApp, Teams, or another OpenClaw-supported surface.

## Purpose

OpenClaw is treated as a channel gateway only. The skill's safety-first mental-care behavior stays the source of truth:

- route crisis and urgent-risk messages before any normal module;
- keep replies non-diagnostic and low burden;
- never provide self-harm methods, concealment help, or medication-change instructions;
- never store mental-health records without explicit consent for that exact record type;
- never put channel bot tokens, provider API keys, or private chat secrets into mental-care local data files.

## One-command bridge install

From this repository:

```bash
bash scripts/install_openclaw.sh --channel telegram --bot-id mental-care-telegram --consent true
```

Optional full gateway bootstrap, when the operator wants this script to run OpenClaw's installer and onboarding:

```bash
bash scripts/install_openclaw.sh --install-gateway --onboard --channel feishu --bot-id feishu-care --consent true
```

The script writes:

- `~/.openclaw/skills/mental-care-skill/` — a local copy of this skill for OpenClaw-side agent instructions.
- `~/.openclaw/agents/mental-care-skill.agent.md` — a concise agent bridge prompt.
- `~/mental_care_data/openclaw_dedicated_bots.json` — non-secret routing metadata for dedicated mental-care bots.

## Dedicated mental-care bot

To designate or update one OpenClaw bot as the mental-care specialist:

```bash
python scripts/configure_openclaw_bot.py set \
  --bot-id mental-care-telegram \
  --channel telegram \
  --display-name "Mental Care" \
  --allowed-user-ids '["123456"]' \
  --consent true
```

To view local routing metadata:

```bash
python scripts/configure_openclaw_bot.py list
```

To remove a bot designation:

```bash
python scripts/configure_openclaw_bot.py unset --bot-id mental-care-telegram --consent true
```

## Local database rules

`openclaw_dedicated_bots.json` is a local database file under the same default data root as other mental-care records. It stores only metadata needed to identify a dedicated mental-care bot:

- bot id and channel name;
- display name and scope;
- optional allowlisted user/chat ids;
- the OpenClaw agent label;
- the system prompt that tells the bot to use this skill.

It must not contain:

- Telegram/Discord/Feishu bot tokens;
- model provider API keys;
- raw therapy-like transcripts;
- crisis details copied from user messages;
- contact methods unless the support-contact workflow explicitly allowed them.

## Confidence loop for OpenClaw changes

At every critical step, ask: "Do I have evidence-backed confidence in this strategy?" Because literal 100% safety cannot be guaranteed for software or mental-health workflows, convert uncertainty into concrete checks:

1. Identify possible holes: token leakage, accidental external sharing, wrong bot routed as specialist, crisis messages handled as normal chat, missing consent, broken local schema.
2. Apply the smallest repair: stricter defaults, allowlists, local-only fields, tests, or clearer operator instructions.
3. Run checks: unit tests, local data validation, and a dry install into temporary OpenClaw/data directories.
4. Repeat until the current patch has no known unmitigated issue and the checks pass.
