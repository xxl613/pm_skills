# project-workspace-init

Initializes a reusable project workspace with a standard `00` to `07` directory
system, root collaboration documents, and per-directory `_README.md` files.

## Use When

- Starting a new project workspace.
- Standardizing an existing project folder without overwriting current files.
- Creating a durable structure for product design, agent capability notes,
  architecture, research, validation, design files, and meeting records.

## Main Output

- `00_项目管理/`
- `01_产品设计/`
- `02_智能体能力/`
- `03_技术架构/`
- `04_业务调研/`
- `05_交付验证/`
- `06_设计文件/`
- `07_会议记录/`
- Root `AGENTS.md`, `MEMORY.md`, and `README.md`
- Main-directory `_README.md` files

## Source

Local source:

```text
/Users/xiaolongxiong/.codex/skills/project-workspace-init
```

Published copy:

```text
pm_skills/project-workspace-init
```

## Notes

This skill is intentionally conservative: it creates missing structure, avoids
business-specific content, and writes `.new.md` candidates instead of overwriting
existing documents.

