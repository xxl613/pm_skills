# PM Skills

这个仓库用于发布本地维护的 Codex skills，重点覆盖产品管理、原型工作流、Figma 转换，以及可复用项目空间初始化。

这些 skill 的日常维护位置仍然在本地目录。本仓库是同步到 GitHub 的发布副本，除非后续明确把某个 skill 迁移到这里作为唯一源头。

## 已包含的 Skills

| Skill | 侧重点 | 路径 |
|:---|:---|:---|
| `project-workspace-init` | 初始化结构化项目空间，用于产品设计、业务调研、交付验证、会议记录等长期协作。 | `pm_skills/project-workspace-init/` |
| `html-prototype-to-figma` | 将 HTML/React/Vite 原型或本地页面转换为可编辑 Figma 设计稿，并进行还原度校验。 | `pm_skills/html-prototype-to-figma/` |
| `figma-prototype-system` | 基于已有 Figma 节点搭建可复用的 React/Vite 原型基础工程，并沉淀设计语言。 | `pm_skills/figma-prototype-system/` |

## 仓库结构

```text
pm_skills/
  project-workspace-init/
  html-prototype-to-figma/
  figma-prototype-system/
pm_skills.manifest.yaml
tools/
  sync_pm_skills.sh
```

## 同步流程

本地源 skill 修改后，在仓库根目录运行：

```bash
./tools/sync_pm_skills.sh
```

然后检查、提交并推送：

```bash
git status
git add pm_skills pm_skills.manifest.yaml tools README.md
git commit -m "Sync PM skills"
git push
```

同步脚本会读取 `tools/sync_pm_skills.sh` 中固定的源路径，并把每个 skill 复制到 `pm_skills/`。每个 skill 目录里的 `README.md` 是仓库说明文档，会在同步时保留，不会被删除。

## 源路径映射

当前源路径映射记录在 `pm_skills.manifest.yaml`。

如果需要发布新的 skill，需要同时更新：

- `pm_skills.manifest.yaml`
- `tools/sync_pm_skills.sh`

然后运行同步脚本，并在新的 skill 目录下补充一个简短的 `README.md`。

