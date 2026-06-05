# html-prototype-to-figma

定义将 HTML、React、Vite 原型、本地预览站或已渲染网页转换为可编辑 Figma 设计稿的工作流。

## 适用场景

- 将本地原型同步到 Figma。
- 只捕获真实业务界面，排除原型评审工具。
- 把隐藏滚动内容和交互状态展开成 Figma 画板。
- 校验生成的 Figma 结果是否与浏览器源页面一致。
- 排查 Figma MCP 转换、图层可见性、裁剪、层级或素材问题。

## 关注重点

- 写入 Figma 前先确认目标文件。
- 只捕获真实用户会看到的产品 UI。
- 排除 PRD 面板、路由目录、调试控件和评审辅助界面。
- 使用 Figma MCP `generate_figma_design` 的 `captureId` + HTML-to-design 捕获脚本流程，而不是把截图或 image fill 当成最终交付。
- 使用明确的浏览器视口尺寸；默认桌面画板最终保持 `1440px` 宽。
- 捕获时通过 `.figma-page`、`main[data-capture-root]` 等业务根节点 selector 排除原型外壳。
- 保留完整滚动内容和关键交互状态。
- 保持页面名称与原型页面名称一致。
- 不要默认对可编辑 HTML-to-Figma 结果整树执行 `frame.rescale(...)`。先对比源 CSS/DOM 与 Figma 中的容器宽度、文字字号、图标尺寸；只有所有元素共享同一缩放比例时才允许整体缩放。
- 特别检查“假性正确”的 `1440px` 画板：外框看似正确，但文字可能从源页面 `12px` 变成 Figma `7px`，图标可能从 `18px` 变成 `10px`。
- 在确认完成前，对比浏览器截图和 Figma 截图。

## 标准交付检查

每次把 HTML 原型同步到 Figma 后，至少确认：

- 每个页面或状态使用独立的 `captureId`，并轮询到完成。
- 临时捕获脚本已移除，除非明确需要保留给人工复捕。
- Figma 结果包含可编辑文本、矢量或分组图层，不是单张截图。
- 根画板宽度、核心卡片/输入框尺寸、文字字号和图标尺寸都与源页面一致。
- 页面目录、PRD 信息、变更记录、调试控件等原型辅助 UI 没有进入最终画板。

## 源路径

本地源目录：

```text
/Users/xiaolongxiong/.codex/skills/html-prototype-to-figma
```

仓库发布副本：

```text
pm_skills/html-prototype-to-figma
```

## 相关 Skills

- `figma:figma-use`
- `figma:figma-generate-design`
- `figma-mcp-troubleshooting`
