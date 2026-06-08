# figma-to-html-replica

定义将 Figma 画板高保真复刻为 HTML/CSS 或项目栈页面的工作流，并通过 Figma 截图与浏览器截图对比持续校准视觉差异。

## 适用场景

- 将指定 Figma 画板还原成可运行页面。
- 把 Figma 设计稿高保真落地为静态 HTML、CSS，或现有 React/Vue/Vite 项目组件。
- 用截图对比验证 HTML 页面与 Figma 画板是否对齐。
- 排查复刻中的字体、间距、图标、图片、mask、徽标或装饰素材缺失问题。
- 在最多 5 轮内按差异清单逐项修正页面。

## 关注重点

- 默认以 1:1 视觉复刻为验收目标。
- 先锁定 `fileKey`、`nodeId` 和画板尺寸，再拉取 Figma 结构和截图。
- 设计稿中可见的图片、SVG、mask、徽标、图标、头像、插画和纹理都要建立资产清单。
- 关键可见资产必须本地化，不能依赖 Figma MCP 临时 URL。
- 下载资产后要校验真实格式，避免 SVG 内容被错误保存成 `.png`。
- 禁止用占位色块、临时几何图形、伪 icon 或 emoji 冒充真实资产。
- 每轮都要使用同尺寸策略生成 Figma 截图和 HTML 截图，并输出差异说明。
- 未完成至少一轮双端截图对比前，不宣称已完成 1:1 复刻。

## 标准交付检查

每次执行 Figma 到 HTML 复刻后，至少确认：

- 已记录 Figma 来源、画板尺寸和目标页面入口。
- 已建立并落地可见资产清单。
- 所有关键资产已本地化并通过格式校验。
- HTML 页面在目标视口下可打开、图片加载完整、无结构性错位。
- 已保存同尺寸 Figma 截图和 HTML 截图。
- 已完成差异分析，或说明剩余差异和阻塞原因。
- 当前迭代轮次不超过 5 轮。

## 源路径

本地源目录：

```text
/Users/xiaolongxiong/.codex/skills/figma-to-html-replica
```

仓库发布副本：

```text
pm_skills/figma-to-html-replica
```

## 相关 Skills

- `figma:figma-use`
- `figma:figma-generate-design`
- `figma-mcp-troubleshooting`
- `html-prototype-to-figma`
