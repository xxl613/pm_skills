---
name: project-workspace-init
description: Use when initializing a new or existing project workspace with a structured 00-08 directory system, AGENTS.md, MEMORY.md, README.md, per-directory _README.md files, and an 08_LLM_WIKI compilation layer. Use when the user wants a reusable, non-overwriting workspace foundation for sustained product, design, research, validation, meeting-record iteration, and AI-readable project knowledge digestion. Also use when an existing workspace feels cluttered and needs the standard file-lifecycle rules (per-directory _archive/, _README inventory, deletion/archive criteria) added to its AGENTS.md.
---

# Project Workspace Init

Initialize a project workspace with a reusable collaboration structure. Keep the structure project-generic and never copy business content from another project.

## Core Rules

- Create only the `00` to `08` project directories listed below.
- Do not create `docs/superpowers/`.
- Do not create `temp/`.
- Do not create a prototype project.
- Do not create databases, vector stores, search indexes, background watchers, local services, or automation scripts for the LLM Wiki layer.
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
08_LLM_WIKI/
08_LLM_WIKI/00_入口/
08_LLM_WIKI/01_当前口径/
08_LLM_WIKI/02_产品对象/
08_LLM_WIKI/03_PRD与需求/
08_LLM_WIKI/04_原型与页面/
08_LLM_WIKI/05_会议与决策/
08_LLM_WIKI/06_来源登记/
```

Create these root files from `templates/`:

```text
AGENTS.md
MEMORY.md
README.md
```

Create the project status dashboard from `templates/current-status.md`:

```text
00_项目管理/当前项目状态与待办.md
```

Create `_README.md` in each original material main directory from `templates/directory-readme.md`:

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

Create the minimum useful LLM Wiki files from `templates/llm-wiki/`:

```text
08_LLM_WIKI/00_入口/README.md
08_LLM_WIKI/00_入口/SCHEMA.md
08_LLM_WIKI/00_入口/index.md
08_LLM_WIKI/00_入口/log.md
08_LLM_WIKI/01_当前口径/稳定决策.md
08_LLM_WIKI/01_当前口径/候选结论.md
08_LLM_WIKI/01_当前口径/待确认问题.md
08_LLM_WIKI/06_来源登记/source-register.md
08_LLM_WIKI/06_来源登记/file-digests.md
```

## Directory Responsibilities

| Directory | Responsibility |
|:---|:---|
| `00_项目管理/` | Project background, goals, phase plan, open questions, milestones, collaboration information; `当前项目状态与待办.md` is the single dashboard entry for project status, scope, todos, and timeline |
| `01_产品设计/` | PRDs, requirement pool, user stories, feature specs, glossary, product rules |
| `02_智能体能力/` | Agent, Skill, MCP, workflow, tool capability, and capability asset notes |
| `03_技术架构/` | Architecture diagrams, technical plans, data structures, interface boundaries, system dependencies |
| `04_业务调研/` | Interviews, competitor research, business materials, raw research notes |
| `05_交付验证/` | Demo acceptance, test records, issue lists, delivery materials, review feedback |
| `06_设计文件/` | `DESIGN.md`, prototype projects, Figma materials, screenshots, visual rules, page catalog, PRD reference layer, change records, design deliverables |
| `07_会议记录/` | Raw meeting notes, cleaned summaries, meeting conclusions, action items |
| `08_LLM_WIKI/` | AI-readable compilation, task routing, source registration, file digests, candidate conclusions, open questions, and source tracing |

## LLM Wiki Knowledge Lifecycle

Use the LLM Wiki as a manual, traceable knowledge pipeline:

1. Source material enters through `source-register.md` and `file-digests.md`.
2. Inferred but unconfirmed judgments go to `候选结论.md`.
3. Unknowns that need user, client, team, data-source, or stakeholder confirmation go to `待确认问题.md`.
4. User-confirmed conclusions go to `稳定决策.md` and, when they affect future work, `MEMORY.md` or the relevant formal document.
5. Confirmed questions are removed from the current open-question list. Do not keep `已确认` items in `待确认问题.md`.
6. Historical identifiers are never renumbered or reused after promotion, deletion, rejection, or closure.

Use stable identifiers:

| File | Identifier | Rule |
|:---|:---|:---|
| `候选结论.md` | `C-001`, `C-002` | Each candidate conclusion gets a stable `C-` number. When confirmed, record the original candidate number in `稳定决策.md`. |
| `待确认问题.md` | `Q-001`, `Q-002` | Each open question gets a stable `Q-` number. When confirmed, remove it from the current list and record the original question number in `稳定决策.md`. |
| `稳定决策.md` | Title + source number | Stable decisions record the confirmed conclusion plus any original `C-` or `Q-` references. |
| `当前项目状态与待办.md` | `T-001`, `T-002` | Each todo gets a stable `T-` number. Completed todos move to the archive section at the end of the same file with a completion date. Numbers are never renumbered or reused. |

Conceptual distinction:

- `候选结论` is an inferred judgment from materials. It is useful for discussion but cannot be treated as project fact.
- `待确认问题` is a live blocker or uncertainty that still needs an answer.
- `稳定决策` is confirmed project truth that future PRDs, prototypes, delivery notes, and memory can reuse.

## File Lifecycle Management

The generated `AGENTS.md` defines a file lifecycle so the workspace stays clean over time. Files are 活跃, 归档, or deleted:

- **Archive**: each main directory gets an `_archive/` for files not needed short-term but still valuable. Created on demand only — never pre-create empty `_archive/` directories at init. When first archiving into a directory, create `_archive/_README.md` from `templates/archive-readme.md` as the ledger (original path, archive date, reason, deletion condition per file). Archived files keep their original names. Default reading paths skip `_archive/` unless the user asks for history.
- **Delete**: only via a cleanup proposal (🟢delete / 🟡archive / 🔴keep, each with a reason) confirmed by the user — never silently. Deletion candidates: regenerable outputs (share bundles, `dist/`, `node_modules/`), intermediate drafts (including merged/abandoned `.new.md` files), and expired content (superseded by a confirmed newer version, fully merged into a formal document, or unreferenced one full phase after its milestone shipped). Before deleting a regenerable output, record how to regenerate it in the directory's `_README.md`. When unsure, archive instead of delete.
- **Inventory**: each `_README.md` holds a one-line-per-file inventory table (file / purpose / status / last-updated) that serves as the directory's query entry. Any session that adds, moves, archives, or deletes files in a directory must sync that directory's `_README.md` before ending — same duty style as the status dashboard sync.
- **Anti-redundancy**: formal documents are updated in place with in-file revision logs; parallel copies like `xxx-v2.md` / `xxx-最终版.md` are forbidden. Old versions go to `_archive/` the same day. `.new.md` candidates are deleted immediately after being merged or rejected.
- **Trigger**: at each milestone close, run a directory inspection (inventory accuracy + archive/delete candidates) and sync results to `00_项目管理/当前项目状态与待办.md`.

These rules live in the generated `AGENTS.md` section 6; this skill only seeds them and the matching `_README.md` inventory structure.

## Project Status Dashboard

`00_项目管理/当前项目状态与待办.md` is the single dashboard entry for "what is this project, what am I doing, what is the timeline". It answers three reader questions in order: project identity (项目简介: a 3-5 sentence prose introduction a first-time reader can absorb in 30 seconds, plus a fact table), schedule (时间与里程碑, milestone granularity only), and work state (当前范围 / 当前待办 / 关键产出物状态 / 下一步建议). A fuller onboarding document may live at `00_项目管理/项目介绍.md`; the dashboard intro stays short and links to it instead of duplicating it.

Dashboard rules:

- It is an aggregation view, not a source of truth. Full lists stay in their own files; the dashboard links to them in 关联文件.
- 阻塞与待确认 holds only blocking-level questions (reusing their `Q-` numbers). The full open-question list lives only in `08_LLM_WIKI/01_当前口径/待确认问题.md` and is never duplicated in full.
- Todos use stable `T-` numbers. Completed todos move to the 已完成归档 section at the end of the file with a completion date; numbers are never renumbered or reused.
- Any session that changes scope, todos, milestones, deliverable status, or blocking questions must sync this file before ending and refresh `最后更新`. This duty is written into the generated `AGENTS.md`.

## Workflow

1. Determine the target project directory.
   - Use the user-provided path when available.
   - Otherwise use the current working directory.

2. Inspect the target directory.
   - Identify existing root files and main directories.
   - Continue even if the directory is not empty.

3. Create missing directories.
   - Create missing original material directories from `00_项目管理/` through `07_会议记录/`.
   - Create missing `08_LLM_WIKI` compilation-layer directories.
   - Existing directories are fine and should be left untouched.

4. Create root documents.
   - If `AGENTS.md` is missing, create it from `templates/AGENTS.md`; otherwise create `AGENTS.new.md`.
   - If `MEMORY.md` is missing, create it from `templates/MEMORY.md`; otherwise create `MEMORY.new.md`.
   - If `README.md` is missing, create it from `templates/README.md`; otherwise create `README.new.md`.
   - If `00_项目管理/当前项目状态与待办.md` is missing, create it from `templates/current-status.md`; otherwise create `当前项目状态与待办.new.md`.
   - Fill the dashboard's `最后更新` with the current date. Fill other placeholders only from confirmed project facts; keep unknown fields as explicit placeholders.

5. Create directory readmes.
   - For each original material main directory from `00_项目管理/` through `07_会议记录/`, create `_README.md`.
   - If `_README.md` exists, create `_README.new.md`.
   - Replace template placeholders with the directory name, responsibility, what belongs there, what does not belong there, and common examples.
   - Keep the 文件清单 inventory table; when the directory already contains files, fill one row per existing file or subdirectory (one-line purpose, 状态, date), otherwise leave the 暂无 placeholder row.
   - Do not pre-create `_archive/` directories; they are created on demand from `templates/archive-readme.md` when the first file is archived.

6. Create LLM Wiki files.
   - Create each minimum useful LLM Wiki file from `templates/llm-wiki/`.
   - If a target LLM Wiki file exists, create the matching `.new.md` candidate.
   - Keep LLM Wiki files project-generic until the user asks to digest real project materials.
   - Ensure candidate conclusions and open questions use numbered templates: `C-001` for candidates and `Q-001` for questions.

7. Report the result.
   - List created directories.
   - List created files.
   - List LLM Wiki files created from `templates/llm-wiki/`.
   - List candidate `.new.md` files caused by existing files.
   - Tell the user to fill in `MEMORY.md` project positioning and current delivery goals next, then start digesting important existing files into `08_LLM_WIKI`.

## Template Use

Use these bundled templates:

- `templates/AGENTS.md`: root collaboration rules.
- `templates/MEMORY.md`: project memory skeleton.
- `templates/README.md`: workspace navigation.
- `templates/current-status.md`: project status dashboard for `00_项目管理/当前项目状态与待办.md`.
- `templates/directory-readme.md`: per-directory `_README.md` skeleton with the 文件清单 inventory table.
- `templates/archive-readme.md`: `_archive/_README.md` ledger skeleton, used on demand when the first file is archived — not at init.
- `templates/llm-wiki/`: minimum useful skeleton files for `08_LLM_WIKI`.

When filling templates, keep placeholders explicit if the project facts are unknown. Do not invent project positioning, target users, PRD names, prototype paths, or technical architecture.

The LLM Wiki templates are immediately usable as a manual-trigger, rule-driven compilation layer. They do not provide background scanning or automatic source digestion. When a user asks to digest a file, update source registration, file digests, numbered candidate conclusions, and numbered open questions first. Promote conclusions into stable decisions only after explicit user confirmation. Confirmed questions must leave the current open-question list and move into stable decisions, memory, or formal project documents.

## Validation

After initialization, verify:

- This skill created no directories outside the requested `00` to `08` standard structure.
- No `docs/superpowers/` or `temp/` directory was created by this skill.
- Existing files were not overwritten.
- `AGENTS.md`, `MEMORY.md`, `README.md`, or `.new.md` candidates exist.
- `00_项目管理/当前项目状态与待办.md` or `当前项目状态与待办.new.md` exists.
- Each main directory has `_README.md` or `_README.new.md`, containing the 文件清单 inventory table.
- No empty `_archive/` directory was pre-created by this skill.
- `08_LLM_WIKI/00_入口/SCHEMA.md` or `08_LLM_WIKI/00_入口/SCHEMA.new.md` exists.
- `08_LLM_WIKI/00_入口/index.md` or `08_LLM_WIKI/00_入口/index.new.md` exists.
- `08_LLM_WIKI/01_当前口径/候选结论.md` or `08_LLM_WIKI/01_当前口径/候选结论.new.md` exists.
- `08_LLM_WIKI/06_来源登记/source-register.md` or `08_LLM_WIKI/06_来源登记/source-register.new.md` exists.
- No database, vector store, search index, watcher, local service, automation script, prototype project, or dependency install was created by this skill.
