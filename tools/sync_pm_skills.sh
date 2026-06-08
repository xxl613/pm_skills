#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sync_skill() {
  local name="$1"
  local source_dir="$2"
  local target_dir="$3"

  if [[ ! -d "$source_dir" ]]; then
    echo "Missing source for $name: $source_dir" >&2
    return 1
  fi

  if [[ ! -f "$source_dir/SKILL.md" ]]; then
    echo "Missing SKILL.md for $name: $source_dir/SKILL.md" >&2
    return 1
  fi

  mkdir -p "$(dirname "$ROOT_DIR/$target_dir")"
  rsync -a --delete \
    --exclude '.DS_Store' \
    --exclude 'README.md' \
    "$source_dir/" \
    "$ROOT_DIR/$target_dir/"

  echo "Synced $name -> $target_dir"
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
