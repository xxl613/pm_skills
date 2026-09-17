#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[[ $# -le 1 ]] || { echo "Usage: $0 [skill-name]" >&2; exit 2; }
SELECTED_SKILL="${1:-}"
SYNCED_COUNT=0

sync_skill() {
  local name="$1"
  local source_dir="$2"
  local target_dir="$3"
  local sync_options=(-a --delete)

  [[ -z "$SELECTED_SKILL" || "$SELECTED_SKILL" == "$name" ]] || return 0

  if [[ ! -d "$source_dir" ]]; then
    echo "Missing source for $name: $source_dir" >&2
    return 1
  fi

  if [[ -f "$source_dir/.codex-plugin/plugin.json" && -f "$source_dir/skills/$name/SKILL.md" ]]; then
    # Plugin resources use package-relative paths; copy the complete package.
    :
  elif [[ ! -f "$source_dir/SKILL.md" ]]; then
    echo "Missing SKILL.md for $name: $source_dir/SKILL.md" >&2
    return 1
  else
    sync_options+=(--exclude '/README.md')
  fi

  mkdir -p "$(dirname "$ROOT_DIR/$target_dir")"
  rsync "${sync_options[@]}" \
    --exclude '.DS_Store' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.git/' \
    --exclude 'node_modules/' \
    "$source_dir/" \
    "$ROOT_DIR/$target_dir/"

  echo "Synced $name -> $target_dir"
  SYNCED_COUNT=$((SYNCED_COUNT + 1))
}

sync_skill "project-workspace-init" \
  "/Users/xiaolongxiong/.codex/skills/project-workspace-init" \
  "pm_skills/project-workspace-init"

sync_skill "html-prototype-to-figma" \
  "/Users/xiaolongxiong/.codex/skills/html-prototype-to-figma" \
  "pm_skills/html-prototype-to-figma"

sync_skill "figma-prototype-system" \
  "/Users/xiaolongxiong/.codex/skills/figma-prototype-system" \
  "pm_skills/figma-prototype-system"

sync_skill "figma-to-html-replica" \
  "/Users/xiaolongxiong/.codex/skills/figma-to-html-replica" \
  "pm_skills/figma-to-html-replica"

sync_skill "prd-writing-style" \
  "/Users/xiaolongxiong/PycharmProjects/ai_group/.agents/skills/prd-writing-style" \
  "pm_skills/prd-writing-style"

sync_skill "html-prototype-style" \
  "/Users/xiaolongxiong/PycharmProjects/ai_group/.agents/skills/html-prototype-style" \
  "pm_skills/html-prototype-style"

sync_skill "v5-page-planning" \
  "/Users/xiaolongxiong/.codex/skills/v5-page-planning" \
  "pm_skills/v5-page-planning"

sync_skill "v5-ux-rule" \
  "/Users/xiaolongxiong/.codex/skills/v5-ux-rule" \
  "pm_skills/v5-ux-rule"

sync_skill "prototype-studio" \
  "/Users/xiaolongxiong/plugins/prototype-studio" \
  "pm_skills/prototype-studio"

[[ "$SYNCED_COUNT" -gt 0 ]] || { echo "Unknown skill: $SELECTED_SKILL" >&2; exit 2; }
