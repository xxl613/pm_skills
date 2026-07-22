# PM Skills

这个仓库用于发布本地维护的 Codex skills，重点覆盖产品管理、原型工作流、Figma 转换，以及可复用项目空间初始化。

这些 skill 的日常维护位置仍然在本地目录。本仓库是同步到 GitHub 的发布副本，除非后续明确把某个 skill 迁移到这里作为唯一源头。

## 已包含的 Skills

| Skill | 侧重点 | 路径 |
|:---|:---|:---|
| `project-workspace-init` | 初始化结构化项目空间，用于产品设计、业务调研、交付验证、会议记录等长期协作。 | `pm_skills/project-workspace-init/` |
| `html-prototype-to-figma` | 将 HTML/React/Vite 原型或本地页面转换为可编辑 Figma 设计稿，并进行还原度校验。 | `pm_skills/html-prototype-to-figma/` |
| `figma-prototype-system` | 基于已有 Figma 节点搭建可复用的 React/Vite 原型基础工程，并沉淀设计语言。 | `pm_skills/figma-prototype-system/` |
| `figma-to-html-replica` | 将 Figma 画板高保真复刻为 HTML/CSS 或项目栈页面，并通过截图对比迭代缩小视觉差异。 | `pm_skills/figma-to-html-replica/` |
| `prd-writing-style` | 教师中心 PRD、功能说明、需求池和研发对齐文档的写作与改写风格。 | `pm_skills/prd-writing-style/` |
| `html-prototype-style` | HTML/React 原型页面绘制和修改的质量约束，适用于框架页面、卡片、弹窗、抽屉流程和状态机制。 | `pm_skills/html-prototype-style/` |
| `v5-page-planning` | 将带 ID 的结构化需求参数清单拆成可追溯的页面地图、参数覆盖矩阵和逐页规划文档。 | `pm_skills/v5-page-planning/` |
| `v5-ux-rule` | 大明白 V5 定制原型的桌面端与移动端通用 UX 规范、壳层、组件和项目建档资产。 | `pm_skills/v5-ux-rule/` |

## 仓库结构

```text
pm_skills/
  project-workspace-init/
  html-prototype-to-figma/
  figma-prototype-system/
  figma-to-html-replica/
  prd-writing-style/
  html-prototype-style/
  v5-page-planning/
  v5-ux-rule/
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
