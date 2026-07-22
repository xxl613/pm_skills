# 06 · 从 Figma 剥离设计语言（路线甲 · 皮肤级）

适用：保留 v5-ux-rule 的**结构/UX**，只把**视觉**换成项目自有 Figma 的设计语言。
产出 = 项目档案的 `DESIGN.md`（人可读真源）+ `theme.css`（令牌投影）。
**不动壳层/组件结构**；若连布局/组件骨架都不同，那是整套 bootstrap（用 figma-prototype-system），不走本流程。

## 前提（实测坑）
- Figma Desktop 开 **Dev Mode**，把**目标画板设为当前活动页签**（MCP 只读当前活动页签）。
- Figma MCP 可能中途掉线 → 需重启 Claude Code 重连；卡住见 `figma-mcp-troubleshooting`。
- 资产落盘受 Allowed-directories 限制（本流程主要取值，不一定落盘资产）。

## 步骤
1. **取变量/样式**（Figma MCP）：
   - `get_variable_defs` → 颜色变量、间距、圆角等 design variables。
   - `get_design_context` → 文本样式（字号/行高/字重/标题层级）、effect（阴影）。
   - 需要肉眼核对时 `get_screenshot` 截目标节点。
2. **填 DESIGN.md**：
   - §1–§6 写人可读设计语言（色/字/阶梯/间距的**理由与用法**，引用令牌名，不重复写值）。
   - **§8 令牌之外**：把 CSS 表达不了的固化下来——标题阶梯、hover/focus/disabled、近黑按钮 vs 品牌蓝 CTA 的角色、新造组件范式、动效、纪律与反例。
   - **§9 令牌契约**：在 ```css :root{}``` 块里写本项目**覆盖/新增**的令牌（含值）。这是机器源。
3. **同步 theme.css**：把 §9 契约**逐条**写进 `theme.css`（覆盖 v5 base；base 没有的如标题阶梯由它新增）。§9 与 theme.css 应一致。
4. **校验 + 自检**：
   - `python3 check-design.py --check` → ①漏实现/②野令牌/③值漂移 须为 0。
   - 页面已引 `tokens.css → theme.css`；截图比对 UI 是否已变成目标设计语言。

## Figma → `--v5-*` 令牌映射表
| Figma 来源 | DESIGN.md 段 | theme.css 令牌 |
|---|---|---|
| 品牌主色 | §1 | `--v5-color-brand`（连带 `--v5-color-info` 若同色） |
| 成功/警告/错误语义色 | §1 | `--v5-color-success` / `-warning` / `-error`（浅底 `*-bg`） |
| 页面背景 / 表面 / 描边 | §1 | `--v5-color-bg` / `-surface` / `-border` |
| 文本主/次/三级/禁用 | §1 | `--v5-color-text` / `-secondary` / `-tertiary` / `-disabled` |
| 浅填充 | §1 | `--v5-color-fill` |
| 字体族 | §2 | `--v5-font-family` |
| 区块标题/正文/说明 字号·行高 | §3 | `--v5-font-size-title|body|caption` + `--v5-line-height-*` |
| 更细标题阶梯 H1–H6 | §4 | **新增** `--v5-font-size-h1…`（base 无，theme 扩展） |
| 间距阶梯 | §5 | `--v5-space-1..6`（一般沿用，改了才覆盖） |
| 圆角 | §5 | `--v5-radius-sm|md|lg|pill` |
| 阴影 | §5 | `--v5-shadow-card` / `--v5-shadow-overlay` |

## 同步纪律
- **DESIGN.md ⟷ theme.css 必须同步**：DESIGN.md 是真源，改它就改 theme.css（同导航母版↔拷贝）。
- theme.css 只放**差异**；与 base 相同的值别照抄，保证 base 升级能流下来。
- 不要把视觉值散落进页面内联样式 —— 一律走令牌。
