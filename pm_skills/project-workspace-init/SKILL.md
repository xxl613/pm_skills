---
name: project-workspace-init
description: Use when initializing a new or existing project workspace with a structured 00-07 directory system, AGENTS.md, MEMORY.md, README.md, and per-directory _README.md files. Use when the user wants a reusable, non-overwriting workspace foundation for sustained product, design, research, validation, and meeting-record iteration.
---

# Project Workspace Init

Initialize a project workspace with a reusable collaboration structure. Keep the structure project-generic and never copy business content from another project.

## Core Rules

- Create only the `00` to `07` project directories listed below.
- Do not create `docs/superpowers/`.
- Do not create `temp/`.
- Do not create a prototype project.
- Do not initialize git, commit, install dependencies, or modify unrelated files.
- Never overwrite existing files. If a target file exists, create the `.new.md` candidate described below.
- Keep generated documents project-generic until the user provides confirmed project facts.

## Target Structure

Create these directories:

```text
00_项目管理/
00_项目管理/待确认问题/
01_产品设计/
01_产品设计/需求详情/
02_智能体能力/
03_技术架构/
03_技术架构/images/
04_业务调研/
04_业务调研/访谈文稿/
05_交付验证/
05_交付验证/验收记录/
06_设计文件/
06_设计文件/images/
07_会议记录/
07_会议记录/原始会议记录/
07_会议记录/整理后会议纪要/
```

Create these root files from `templates/`:

```text
AGENTS.md
MEMORY.md
README.md
```

Create `_README.md` in each main directory from `templates/directory-readme.md`:

```text
00_项目管理/_README.md
01_产品设计/_README.md
02_智能体能力/_README.md
03_技术架构/_README.md
04_业务调研/_README.md
05_交付验证/_README.md
06_设计文件/_README.md
07_会议记录/_README.md
```

## Directory Responsibilities

| Directory | Responsibility |
|:---|:---|
| `00_项目管理/` | Project background, goals, phase plan, open questions, milestones, collaboration information |
| `01_产品设计/` | PRDs, requirement pool, user stories, feature specs, glossary, product rules |
| `02_智能体能力/` | Agent, Skill, MCP, workflow, tool capability, and capability asset notes |
| `03_技术架构/` | Architecture diagrams, technical plans, data structures, interface boundaries, system dependencies |
| `04_业务调研/` | Interviews, competitor research, business materials, raw research notes |
| `05_交付验证/` | Demo acceptance, test records, issue lists, delivery materials, review feedback |
| `06_设计文件/` | `DESIGN.md`, prototype projects, Figma materials, screenshots, visual rules, page catalog, PRD reference layer, change records, design deliverables |
| `07_会议记录/` | Raw meeting notes, cleaned summaries, meeting conclusions, action items |

## Workflow

1. Determine the target project directory.
   - Use the user-provided path when available.
   - Otherwise use the current working directory.

2. Inspect the target directory.
   - Identify existing root files and main directories.
   - Continue even if the directory is not empty.

3. Create missing directories.
   - Existing directories are fine and should be left untouched.

4. Create root documents.
   - If `AGENTS.md` is missing, create it from `templates/AGENTS.md`; otherwise create `AGENTS.new.md`.
   - If `MEMORY.md` is missing, create it from `templates/MEMORY.md`; otherwise create `MEMORY.new.md`.
   - If `README.md` is missing, create it from `templates/README.md`; otherwise create `README.new.md`.

5. Create directory readmes.
   - For each `00` to `07` main directory, create `_README.md`.
   - If `_README.md` exists, create `_README.new.md`.
   - Replace template placeholders with the directory name, responsibility, what belongs there, what does not belong there, and common examples.

6. Report the result.
   - List created directories.
   - List created files.
   - List candidate `.new.md` files caused by existing files.
   - Tell the user to fill in `MEMORY.md` project positioning and current delivery goals next.

## Template Use

Use these bundled templates:

- `templates/AGENTS.md`: root collaboration rules.
- `templates/MEMORY.md`: project memory skeleton.
- `templates/README.md`: workspace navigation.
- `templates/directory-readme.md`: per-directory `_README.md` skeleton.

When filling templates, keep placeholders explicit if the project facts are unknown. Do not invent project positioning, target users, PRD names, prototype paths, or technical architecture.

## Validation

After initialization, verify:

- The target contains only the requested `00` to `07` standard directories from this skill.
- No `docs/superpowers/` or `temp/` directory was created by this skill.
- Existing files were not overwritten.
- `AGENTS.md`, `MEMORY.md`, `README.md`, or `.new.md` candidates exist.
- Each main directory has `_README.md` or `_README.new.md`.
