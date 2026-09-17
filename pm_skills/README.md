# 已发布的 PM Skills

这个目录存放从本地同步过来的 Codex skill 发布副本。

每个子目录通常包含：

- `SKILL.md`：真正的 skill 指令文件。
- `README.md`：面向人的说明文档，解释这个 skill 的用途和源路径。
- 可选支持文件，例如 `agents/`、`references/`、`templates/` 或 `scripts/`。

源 skill 仍然保留在原本的本地目录中。提交更新前，在仓库根目录运行同步脚本：

```bash
./tools/sync_pm_skills.sh
```

当前同步的 skill 列表见 `../pm_skills.manifest.yaml`。

`prototype-studio/` 是完整插件包，6 个技能位于其 `skills/` 子目录，公共资源位于包根目录。使用时保留完整目录结构，入口见 [原型工作室](prototype-studio/skills/prototype-studio/SKILL.md)。单独更新可运行 `./tools/sync_pm_skills.sh prototype-studio`（从仓库根目录执行）。

## 当前包含

- `prototype-studio`（含 `prototype-spec`、`prototype-build`、`prototype-components`、`prototype-qa`、`prototype-delivery`）
- `project-workspace-init`
- `html-prototype-to-figma`
- `figma-prototype-system`
- `figma-to-html-replica`
- `prd-writing-style`
- `html-prototype-style`
- `v5-page-planning`
- `v5-ux-rule`
