# Published PM Skills

This directory contains the published copies of selected local Codex skills.

Each child directory should include:

- `SKILL.md`: the actual skill instruction file.
- `README.md`: a human-facing summary of the skill and its source mapping.
- Optional support files such as `agents/`, `references/`, `templates/`, or
  `scripts/`.

Source skills remain in their original local locations. Run the sync script from
the repository root before committing updates:

```bash
./tools/sync_pm_skills.sh
```

Current synced skills are listed in `../pm_skills.manifest.yaml`.

## Included Skills

- `project-workspace-init`
- `html-prototype-to-figma`
- `figma-prototype-system`
