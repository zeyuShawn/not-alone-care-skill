#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="mental-care-skill"
INSTALL_CODEX=1
IDE_LIST="all"
TARGET_DIR="$(pwd)"
SOURCE_DIR="${MENTAL_CARE_INSTALL_SOURCE_DIR:-}"

usage() {
  cat <<'USAGE'
Install mental-care-skill for Codex and AI IDE instruction files.

Usage:
  bash scripts/install.sh [--target DIR] [--ide all|agents,vscode,cursor,trae,tare] [--skip-codex] [--source-dir DIR]

Examples:
  bash scripts/install.sh --ide all --target "$PWD"
  bash scripts/install.sh --ide vscode,cursor --skip-codex --target /path/to/project

Environment:
  MENTAL_CARE_INSTALL_SOURCE_DIR  Source checkout containing SKILL.md, references/, scripts/.
  CODEX_HOME              Codex config root; defaults to ~/.codex.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET_DIR="${2:?--target requires a directory}"
      shift 2
      ;;
    --ide)
      IDE_LIST="${2:?--ide requires a value}"
      shift 2
      ;;
    --skip-codex)
      INSTALL_CODEX=0
      shift
      ;;
    --source-dir)
      SOURCE_DIR="${2:?--source-dir requires a directory}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "$SOURCE_DIR" ]]; then
  SOURCE_DIR="$(cd "$script_dir/.." && pwd)"
fi
SOURCE_DIR="$(cd "$SOURCE_DIR" && pwd)"
TARGET_DIR="$(mkdir -p "$TARGET_DIR" && cd "$TARGET_DIR" && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
CODEX_SKILL_DIR="$CODEX_HOME_DIR/skills/$SKILL_NAME"

require_source() {
  if [[ ! -f "$SOURCE_DIR/SKILL.md" || ! -d "$SOURCE_DIR/references" || ! -d "$SOURCE_DIR/scripts" ]]; then
    echo "Source directory is not a complete $SKILL_NAME checkout: $SOURCE_DIR" >&2
    exit 1
  fi
}

copy_tree() {
  local src="$1"
  local dst="$2"
  mkdir -p "$dst"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete \
      --exclude '.git' \
      --exclude '__pycache__' \
      --exclude '.pytest_cache' \
      "$src/" "$dst/"
  else
    rm -rf "$dst"
    mkdir -p "$(dirname "$dst")"
    cp -R "$src" "$dst"
    rm -rf "$dst/.git" "$dst"/**/__pycache__ 2>/dev/null || true
  fi
}

instruction_body() {
  cat <<'BODY'
# You Are Not Alone / mental-care-skill

Activate these instructions only when the user explicitly asks to use `mental-care-skill`, asks for safety-first mental-health support, or requests the included low-burden outing / career-clarification workflows. Do not change unrelated coding behavior.

Core rules:
- This is not diagnosis, therapy, emergency care, or medication advice.
- Route safety first: immediate danger, self-harm intent, harm-to-others intent, overdose, severe confusion, or unsafe situations override all optional modules.
- Keep distressed-user interaction low burden: short, warm, concrete, one default next step, at most one key question per turn unless safety requires more.
- Never provide self-harm methods, lethal-means details, concealment advice, or detailed harmful plans.
- Do not save, expose, or transmit local records without explicit consent for that exact record type.
- Keep mental-health logs isolated from outing, career, job, and external-site data.
- Optional outing/career modules may run only after safety routing says they are appropriate.

If Codex skills are available, load `$mental-care-skill`. Otherwise, read the local checkout's `SKILL.md` and relevant `references/*.md` files before answering.
BODY
}

write_if_changed() {
  local path="$1"
  local tmp
  tmp="$(mktemp)"
  cat > "$tmp"
  mkdir -p "$(dirname "$path")"
  if [[ -f "$path" ]] && cmp -s "$tmp" "$path"; then
    rm -f "$tmp"
    echo "unchanged $path"
  else
    mv "$tmp" "$path"
    echo "wrote $path"
  fi
}

append_block() {
  local path="$1"
  local start="<!-- mental-care-skill:start -->"
  local end="<!-- mental-care-skill:end -->"
  local tmp block
  tmp="$(mktemp)"
  block="$(mktemp)"
  cat > "$block"
  mkdir -p "$(dirname "$path")"
  if [[ -f "$path" ]]; then
    awk -v start="$start" -v end="$end" '
      $0 == start {skip=1; next}
      $0 == end {skip=0; next}
      skip != 1 {print}
    ' "$path" > "$tmp"
  else
    : > "$tmp"
  fi
  {
    cat "$tmp"
    if [[ -s "$tmp" ]]; then printf '\n'; fi
    printf '%s\n' "$start"
    cat "$block"
    printf '%s\n' "$end"
  } > "$path"
  rm -f "$tmp" "$block"
  echo "updated $path"
}

contains_ide() {
  local needle="$1"
  [[ "$IDE_LIST" == "all" || ",$IDE_LIST," == *",$needle,"* ]]
}

require_source

if [[ "$INSTALL_CODEX" == "1" ]]; then
  copy_tree "$SOURCE_DIR" "$CODEX_SKILL_DIR"
  echo "installed Codex skill: $CODEX_SKILL_DIR"
fi

if contains_ide agents; then
  instruction_body | append_block "$TARGET_DIR/AGENTS.md"
fi

if contains_ide vscode; then
  instruction_body | append_block "$TARGET_DIR/.github/copilot-instructions.md"
fi

if contains_ide cursor; then
  {
    cat <<'MDC'
---
description: Safety-first mental-health support via mental-care-skill
alwaysApply: false
---

MDC
    instruction_body
  } | write_if_changed "$TARGET_DIR/.cursor/rules/mental-care-skill.mdc"
fi

if contains_ide trae || contains_ide tare; then
  instruction_body | append_block "$TARGET_DIR/.trae/rules/project_rules.md"
fi

cat <<DONE

Done.
- Source: $SOURCE_DIR
- Target project: $TARGET_DIR
- Codex skill: $([[ "$INSTALL_CODEX" == "1" ]] && echo "$CODEX_SKILL_DIR" || echo "skipped")
- IDE bridge files: $IDE_LIST

Open VS Code, Cursor, or Trae in the target project and ask:
  Use \$mental-care-skill to provide safety-first support.
DONE
