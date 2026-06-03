# PM Skills

This repository publishes selected local Codex skills that support product
management, prototype workflow, Figma conversion, and reusable project setup.

The skills are maintained locally and synced into this repository as a GitHub
publishing copy. The repository is not the only source of truth for day-to-day
editing unless a skill has been deliberately moved here.

## Skills

| Skill | Focus | Path |
|:---|:---|:---|
| `project-workspace-init` | Initialize a structured project workspace for product, design, research, validation, and meeting records. | `pm_skills/project-workspace-init/` |
| `html-prototype-to-figma` | Convert HTML/React/Vite prototypes or local pages into editable Figma designs with fidelity checks. | `pm_skills/html-prototype-to-figma/` |
| `figma-prototype-system` | Build a reusable React/Vite prototype foundation from existing Figma nodes and capture the design language. | `pm_skills/figma-prototype-system/` |

## Repository Layout

```text
pm_skills/
  project-workspace-init/
  html-prototype-to-figma/
  figma-prototype-system/
pm_skills.manifest.yaml
tools/
  sync_pm_skills.sh
```

## Sync Workflow

After editing the local source skills, sync this repository from the repository
root:

```bash
./tools/sync_pm_skills.sh
```

Then review, commit, and push:

```bash
git status
git add pm_skills pm_skills.manifest.yaml tools README.md
git commit -m "Sync PM skills"
git push
```

The sync script reads the fixed source paths in `tools/sync_pm_skills.sh` and
copies each skill into `pm_skills/`. Each skill directory's local `README.md` is
kept as repository documentation and is not removed during sync.

## Source Mapping

The current source mapping is documented in `pm_skills.manifest.yaml`.

If a new skill should be published here, add it to both:

- `pm_skills.manifest.yaml`
- `tools/sync_pm_skills.sh`

Then run the sync script and add a short `README.md` inside the new skill folder.

