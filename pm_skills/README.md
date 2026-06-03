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

## 当前包含

- `project-workspace-init`
- `html-prototype-to-figma`
- `figma-prototype-system`

