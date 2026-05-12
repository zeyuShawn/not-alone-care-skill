#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="mental-care-skill"
SOURCE_DIR="${MENTAL_CARE_INSTALL_SOURCE_DIR:-}"
OPENCLAW_HOME_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
DATA_DIR="${MENTAL_CARE_DATA_DIR:-$HOME/mental_care_data}"
INSTALL_GATEWAY=0
RUN_ONBOARD=0
CHANNEL="telegram"
BOT_ID=""
BOT_DISPLAY_NAME="Mental Care Specialist"
CONSENT=""

usage() {
  cat <<'USAGE'
Install the mental-care-skill OpenClaw bridge and optionally designate a channel bot.

Usage:
  bash scripts/install_openclaw.sh [--source-dir DIR] [--openclaw-home DIR] [--data-dir DIR]
                              [--install-gateway] [--onboard]
                              [--channel telegram|discord|feishu|lark|...] [--bot-id ID]
                              [--display-name NAME] [--consent true]

Examples:
  bash scripts/install_openclaw.sh --channel telegram --bot-id mental-care-telegram --consent true
  bash scripts/install_openclaw.sh --install-gateway --onboard --channel feishu --bot-id feishu-care --consent true

Notes:
  - Bot tokens and provider API keys are never stored by this script.
  - --install-gateway runs OpenClaw's official installer command.
  - --onboard runs `openclaw onboard --install-daemon` when the openclaw CLI is available.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source-dir) SOURCE_DIR="${2:?--source-dir requires a directory}"; shift 2 ;;
    --openclaw-home) OPENCLAW_HOME_DIR="${2:?--openclaw-home requires a directory}"; shift 2 ;;
    --data-dir) DATA_DIR="${2:?--data-dir requires a directory}"; shift 2 ;;
    --install-gateway) INSTALL_GATEWAY=1; shift ;;
    --onboard) RUN_ONBOARD=1; shift ;;
    --channel) CHANNEL="${2:?--channel requires a value}"; shift 2 ;;
    --bot-id) BOT_ID="${2:?--bot-id requires a value}"; shift 2 ;;
    --display-name) BOT_DISPLAY_NAME="${2:?--display-name requires a value}"; shift 2 ;;
    --consent) CONSENT="${2:?--consent requires true/yes}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "$SOURCE_DIR" ]]; then
  SOURCE_DIR="$(cd "$script_dir/.." && pwd)"
fi
SOURCE_DIR="$(cd "$SOURCE_DIR" && pwd)"
OPENCLAW_HOME_DIR="$(mkdir -p "$OPENCLAW_HOME_DIR" && cd "$OPENCLAW_HOME_DIR" && pwd)"

if [[ ! -f "$SOURCE_DIR/SKILL.md" || ! -d "$SOURCE_DIR/references" || ! -d "$SOURCE_DIR/scripts" ]]; then
  echo "Source directory is not a complete $SKILL_NAME checkout: $SOURCE_DIR" >&2
  exit 1
fi

if [[ "$INSTALL_GATEWAY" == "1" ]]; then
  curl -fsSL https://openclaw.ai/install.sh | bash
fi

if [[ "$RUN_ONBOARD" == "1" ]]; then
  if ! command -v openclaw >/dev/null 2>&1; then
    echo "openclaw CLI not found; use --install-gateway first or install OpenClaw manually." >&2
    exit 1
  fi
  openclaw onboard --install-daemon
fi

skill_dir="$OPENCLAW_HOME_DIR/skills/$SKILL_NAME"
mkdir -p "$skill_dir"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete --exclude '.git' --exclude '__pycache__' --exclude '.pytest_cache' "$SOURCE_DIR/" "$skill_dir/"
else
  rm -rf "$skill_dir"
  mkdir -p "$(dirname "$skill_dir")"
  cp -R "$SOURCE_DIR" "$skill_dir"
fi

mkdir -p "$OPENCLAW_HOME_DIR/agents"
cat > "$OPENCLAW_HOME_DIR/agents/mental-care-skill.agent.md" <<'AGENT'
# mental-care-skill OpenClaw Agent Bridge

Use `$mental-care-skill` for this agent. This bot is a mental-care specialist: safety-first, non-diagnostic, low-burden, crisis-aware, and local-records-by-consent only.

Hard boundaries:
- Do not diagnose, replace professional care, or give medication-change instructions.
- Crisis and immediate danger override all optional modules.
- Do not save local records without explicit consent for that record type.
- Do not transmit mental-health records to external websites, apps, or job platforms without explicit consent.
- Keep OpenClaw/channel tokens outside mental-care local data files.
AGENT

python "$SOURCE_DIR/scripts/init_local_data.py" --data-dir "$DATA_DIR" >/dev/null
python "$SOURCE_DIR/scripts/configure_openclaw_bot.py" --data-dir "$DATA_DIR" init >/dev/null

if [[ -n "$BOT_ID" ]]; then
  python "$SOURCE_DIR/scripts/configure_openclaw_bot.py" --data-dir "$DATA_DIR" set \
    --bot-id "$BOT_ID" \
    --channel "$CHANNEL" \
    --display-name "$BOT_DISPLAY_NAME" \
    --consent "$CONSENT"
fi

cat <<DONE

Done.
- OpenClaw home: $OPENCLAW_HOME_DIR
- Skill bridge: $skill_dir
- Agent bridge: $OPENCLAW_HOME_DIR/agents/mental-care-skill.agent.md
- Local data: $DATA_DIR

Next OpenClaw steps if not already done:
  openclaw onboard --install-daemon
  openclaw dashboard

Then connect or pair the desired channel bot in OpenClaw and route it to the mental-care-skill agent bridge.
DONE
