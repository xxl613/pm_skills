# figma-reference 基准图说明

本目录的 PNG 为**技能组件/壳层的已验证渲染图**，用作交付前自检时的视觉比对基准
（SKILL 工作流第 7 步 / 99-review-checklist.md）。

注：原始「Figma 直出截图」在一次误删事故中丢失；这些组件本身是对齐 Figma「全自动课程助教 V5」
构建并经截图比对验证的，故其渲染图等价承担「该组件/壳层标准长相」的比对职责。
如需 Figma 直出图，可在 Figma Dev Mode 连通后按节点逐页重新导出（见 figma-mcp-troubleshooting）。

## 移动壳层基准（shell-mobile-*.png）

`shell-mobile-portal.png`（A-m）· `shell-mobile-chat-flow.png`（B-m）· `shell-mobile-sheet.png`（C-m）
为移动壳层的已验证渲染图（Chrome headless 600×860 @2x，画板 375 居中）。
结构基准 = Figma「大平台设计-UI」教师端 app（file `ljg4eVP3elzzx5b2Q8FYdI`）：
首页 `56301:15219` · 对话 `56301:10135` · 动作面板 `56301:11808` · 工具面板 `56301:12470`。
注意该 Figma 是 Polymas 皮肤，**只比结构/尺寸，不比颜色**——颜色以 V5 base 令牌渲染图为准。
