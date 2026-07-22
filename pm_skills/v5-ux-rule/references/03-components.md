# 03 · 通用组件（标准用法）

> 组件是**可复制的冻结资产**（`assets/components/*.html`），固化了关键测量值——直接 copy，别凭描述重画。
> 标「派生」= Figma 无设计、按 V5 风格补充。每个组件都有对应 `figma-reference/*.png` 基准图（派生件除外）。

## dialog 弹窗 · `components/dialog.html`
- **居中规则**：相对视口水平+垂直居中 + 遮罩 `rgba(0,0,0,.45)`。超高内容 `max-height: calc(100vh - 2×space)` + 正文滚动。
- **宽度档位**：sm 144 / md 480(派生) / lg 832。圆角 12（介于 md/lg）。阴影 `--v5-shadow-overlay`，描边 1px `--v5-color-border`，z-index 1000。
- **结构**：头部(标题 16/26 semibold + 关闭，内距 16/24 + 底分隔线) / 正文(内距 24，16/28) / 底部(内距 16/24 + 顶分隔线，操作组**右对齐**，按钮间距 16)。
- **按钮**：主=近黑 `--v5-color-text` 白字；次=浅灰 `--v5-color-fill`。**次（取消）在左、主（确定）在右**，整组右对齐。

## card 卡片 · `components/card.html`
- **扁平**：默认底 `--v5-color-bg`(#f7f8fa) + 1px `--v5-color-border`，圆角 `--v5-radius-lg`(16)，**无投影**；卡内白色内容块用 `--v5-color-surface`。仅 `.v5-card--raised` 抬升态用 `--v5-shadow-card`。
- **内边距** `--v5-space-5`(24)。标题 18/26 semibold；正文 16/28。区间距 16，正文内多块 8。
- **一个外壳 + 槽位**：标签槽 / 头部操作槽 / 内容槽 / 底部操作行槽。**语义变体** `--info/--success/--warning/--error` 只换「描边色+浅底色（`--v5-color-*-bg`）」，结构不变。**勿为每种业务卡各做一份。**
- **这是弹窗/表单场景的卡（`.v5-card`），不是对话流结果卡**——对话流（B 版式）里的卡用下面的 `chat-result-card.html`，两套类名不要混用。

## chat-result-card 对话结果卡/列表项 · `components/chat-result-card.html`（派生）
- **对话流专用**，B 版式 `SLOT: 对话内容区` 一律 copy 这个文件，不是 `card.html`。命名 `.v5-rcard`（区别于 `.v5-card`）。
- 固化了：消息头（`.v5-msg-ai__head` 名称/时间/状态标签竖线分隔）、交接「拍了拍」（`.v5-poke`）、结果卡（`.v5-rcard`，含长段落用的 `.v5-row--block` 变体）、短列表（`.v5-plainlist`/`.v5-li`）、多属性可浏览列表项（`.v5-recolist`/`.v5-reco`，含强调徽章 `.v5-badge-priority` 与弱提示徽章 `.v5-fit` 的区分）、回答完成操作栏（`.v5-msg-actions`）与追问建议（`.v5-followup`）、**卡片统一解剖**（类别标签 `.v5-rcard__label`、左色条块 `.v5-block`、选项行 `.v5-opt`、操作行 `.v5-rcard__acts`+近黑 `.v5-pill--primary`、状态 chip `.v5-status`、日期行 `.v5-reco__row`）。
- 排布规则见 `05-ai-patterns.md`，卡片解剖/形态选型见 `07-card-anatomy.md`；**规则文字之外，具体类名/取值一律以这个文件的实际代码为准**，不要凭文字描述重新拼一套类名。

## button 按钮 · `components/button.html`
- **两种主行动（按场景选，不是冲突）**：
  - **近黑主按钮** `--v5-color-text` 白字 —— 弹窗/卡片/行内确认。
  - **品牌蓝 CTA** `--v5-color-brand` 白字胶囊(`--v5-radius-pill`) —— **页面级主行动**（如「创建课程」「新建助教」）。
- 次按钮：白底 + `--v5-color-border` 描边 + `--v5-color-text-tertiary` 字；或填充变体 `--v5-color-fill` 底。文字按钮：透明 + tertiary 字。危险：`--v5-color-error` 底/字。
- 尺寸档：lg 40 / md 36(默认) / sm 28。圆角默认 `--v5-radius-md`(8)，胶囊型用 `--v5-radius-pill`。hover/disabled 为派生态。

## form 表单控件 · `components/form.html`
- 单行控件统一：高 38 · 白底 · 1px `--v5-color-border` · **胶囊圆角** `--v5-radius-pill` · 横距 12 · 14/22。
- 文字：已填 `--v5-color-text`；占位 `--v5-color-text-disabled`；下拉默认值 `--v5-color-text-tertiary`。
- 控件：输入框 / 下拉(右 chevron) / 搜索(左图标)。态：default(实测) / focus(`--v5-color-brand` 柔环,派生) / error(`--v5-color-error`+下方错误文案,派生) / disabled(底 `--v5-color-bg`,派生)。label 上方 14/22 + 8 间距，必填 * 用 error 色。

## input-composer 输入台 · `components/input-composer.html`
- 对话流底部固定输入台：840 宽 · 白卡 `--v5-radius-lg`(16) + 描边 · 内距 16/16/12。
- 上：占位/正文区（占位 `--v5-color-text-disabled`）。下操作行：左 `+ 附件 / @ 提及`；右 `语音 / 麦克 / 发送`。
- **发送钮**：品牌浅底填充方块 `color-mix(brand 12%, white)` + brand 图标；空态 disabled。
- **带附件态**：输入区上方显示文件 chip（图标+名称+大小+移除）——即「对话中传文件」派生样式。

## history-rail 历史对话轨道 · `components/history-rail.html`
- **适用范围**：1440 桌面端 B / C 标准对话页必用；移动端不使用。结构、CSS 和脚本必须整块 copy，不与顶部历史按钮、常驻历史侧栏、普通下拉菜单或旧 `.v5-minimap` 并存。
- **收起态**：组件锚定 `.v5-main` 右缘并垂直居中，轨道 32×168；固定 16 条消息刻度，普通刻度 24×3，允许 26 / 28 宽度变化，当前刻度 32×3、`#1d2129`。
- **展开态**：hover 或 focus / `focus-within` 展开 300×244 面板，右缘不偏移，8px 内距、16px 圆角；历史行高 38px，列表纵向滚动。带抽屉时 `.v5-main` 是定位容器，因此轨道位于主对话列右缘、抽屉左侧。
- **数据契约**：固定 16 个中性占位项，每项渲染为标题非空、文本与 `title` 一致、可解析且安全的本页查询链接 `<a href="?conversation=NN">`。静态默认仅第 01 项带 `.is-current` 和 `aria-current="page"`，仅第 01 条刻度带 `.current`；初始化器通过 `URLSearchParams` 读取 `conversation`，只接受 `01` 至 `16`，加载后把唯一当前行、当前深色刻度和唯一 `aria-current="page"` 同步到匹配项，缺失或非法值回退 01。查询文本不得注入 HTML。
- **无障碍 / 键盘**：轨道使用 `tabindex="0"` 和 `aria-label="历史对话"`，列表 nav 使用 `aria-label="历史对话列表"`；轨道与行项目都必须有可见 `:focus-visible`，键盘聚焦与 hover 一样展开。按 `Escape` 阻止默认行为并收起面板，焦点留在轨道且不触发滚动；离开组件后恢复可再次展开。
- **模态约束**：小型同步函数配合 `MutationObserver` 检测当前可见的 `[aria-modal="true"]`、`.v5-overlay`、`.v5-modal-mask`。出现时轨道须 `hidden` / `aria-hidden="true"`，轨道和 16 个链接全部移出 Tab 顺序；移除或隐藏后恢复 `tabindex="0"` 和链接默认顺序。历史列表 nav 本身不得声明为模态；无模态页不得受影响。

## file-upload 上传文件 · `components/file-upload.html`
- **A 对话中传文件（忠于 Figma `3695:6968`）**：输入台顶部横排**文件卡 270×70** = 文件类型图标(36) + 名称(截断保留扩展名) + 大小 + **hover 删除**(白 pill 红字)，右侧 `>` 滚动。卡底 `--v5-color-bg`，圆角 `--v5-radius-lg`。
- **B 上传状态机（派生，见 `05-ai-patterns.md`）**：已选 / 上传中(进度条 `--v5-color-brand`) / 解析中 / 失败(`--v5-color-error-bg` 浅红底+重试) / 已发送(精简白卡)。
- 文件类型色用语义色占位（表格=success 绿 / 文档=info 蓝 / 其他=tertiary 灰）；真实产品换业务文件图标资源。
- 注：因 Figma Allowed-directories 限制未落地 `figma-reference/file-upload.png` 基准图；已对照 Figma 实时截图忠实复刻并渲染核对。

## table 表格 · `components/table.html`（派生）
- 扁平：表头底 `--v5-color-bg` + 文字 `--v5-color-text-secondary`，正文行白底，1px `--v5-color-border` 行分隔，外圆角 `--v5-radius-lg`，无投影。
- 单元横内距 16，字号 caption/body。含表头 / 数据行 / 行操作(文字按钮) / **空数据态**（「暂无数据」居中 secondary）。

## pagination 分页 · `components/pagination.html`（派生）
- 页码约 32：默认白底描边 + `--v5-color-text`；**当前页**近黑底 `--v5-color-text` 白字；hover `--v5-color-fill`。
- 上一页/下一页（禁用 `--v5-color-text-disabled`）、省略号、可选「共 N 条/跳至」。

## toast 轻提示 · `components/toast.html`（派生）
- 浮层：白底 + `--v5-shadow-overlay` + `--v5-radius-md`，左侧语义图标/色条，单行文案。
- 四语义态：成功/警告/错误/信息（图标与色条用语义色，文字 `--v5-color-text`）。默认出现位置：顶部居中，距顶 `--v5-space-6`。

## empty-state 空状态 · `components/empty-state.html`（派生）
- 居中：占位图标(64–96) + 说明文案 `--v5-color-text-secondary`(body) + 可选主操作按钮(近黑)。展示纯说明 / 带操作两种。

---

## 选组件速查

| 要做… | 用 |
|---|---|
| 确认/表单弹层 | dialog（次左主右，主近黑） |
| 承载一块内容/AI 回答 | card（扁平，语义变体换边框+底色） |
| 页面级主行动 | button 品牌蓝 CTA；弹窗内确认用近黑 |
| 输入/下拉/搜索 | form（胶囊单行控件） |
| 对话输入 + 传文件 | input-composer / file-upload |
| 桌面对话历史导航 | history-rail（16 条刻度；hover / focus 展开） |
| 列表数据 | table（含空态） + pagination |
| 操作反馈 | toast（四语义） |
| 无数据/初始 | empty-state |
