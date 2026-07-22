---
name: v5-ux-rule
description: "Use when creating, modifying, or reviewing 大明白 V5-style customized prototypes — the standard product's reusable design system, desktop (1440) and mobile H5 (375, 移动端/手机/公众号/小程序壳) alike. Covers page archetypes (home/portal, conversation flow, drawer; mobile TabBar portal, mobile chat, bottom sheet), platform decision (mobile vs desktop), the master shells, design tokens, and components (dialog, card, button, form, table, pagination, toast, empty-state, input composer, file upload). Also covers conversation-first AI patterns: Agent task flows, chat pages, drawer flows, file-upload conversations, long-form AI answers and answer-card placement, multi-agent handoff, thinking/tool/status states. Invoke whenever a customized prototype must match V5's general specs so layout, width/font and interactions stay consistent across projects without manual re-tuning."
---

# V5 UX Rule

把标准产品「大明白 V5」的通用规范固化成可复用资产，让每个定制项目的原型**自动符合规范**——你只需与 AI 沟通**定制部分**，对话框位置/宽度/字号等跨项目稳定，不再反复手工调。

## 核心原则：稳定层 vs 可变层

| 层 | 内容 | 载体 | 怎么用 |
|---|---|---|---|
| **稳定层（直接 copy，禁止重画）** | 设计令牌、页面原型壳层（桌面 A/B/C + 移动 A-m/B-m/C-m）、基础组件 | `assets/` 真实代码 | **复制**，不凭描述重写 |
| **可变层（每次定制）** | 业务名称/对象、页面内容、用哪些组件、AI 卡片如何组合 | `references/` 判断依据 | 与用户沟通，按规则套用 |

> 「位置/宽度/字号反复调」属于稳定层 → 以后是 **copy `tokens.css` 和壳层**，不是重新描述，漂移消失。

## 输入分支（开工前先判断）

本技能有两种驱动来源，**先判断用哪种**：

- **A · 规划驱动（指明了页面规划文档时）**：用户提供了 `v5-page-planning` 产出的页面规划文档（`页面-NN-xxx.md`，或项目里的 `06_设计文件/page-plans/<…>/` 目录），**以它为准、按它的内容执行**：
  - **版式**：直接采用规划文档的「版式」字段，**跳过决策树**（上游已定，不再自行判断、不得改判）。
  - **区域 × 内容**：按规划文档的「区域 × 内容」表逐区填槽位，组件用它指明的 `components/*`。
  - **布局参考**：规划文档的 `.layout.png` / `.wireframe.html` 作为分区与信息结构的参考。
  - **覆盖自检**：用规划文档的「满足的参数清单」核对原型是否真的覆盖了这些参数。
  - 其余（copy 稳定层、套交互/文案/AI 规则、截图自检）照下面工作流照常做。
- **B · 规范驱动（未指明页面规划文档时）**：按下面默认工作流执行——自行判断页面原型等。

> 一句话：**指明页面规划文档 → 按文档执行（版式等以文档为准）；不指明 → 按默认规范执行。** 两者都仍 copy 稳定层、禁重画。

## 平台判定（先于版式判断：逐页决定移动还是桌面）

每个页面开画前**先定平台**。按以下顺序取第一个可靠答案，Agent 需要利用已有证据自主判断，不把正常判端工作转交给用户：

1. **用户明确指定**：用户对当前页面或页面类别明确说 PC、桌面、移动端、手机、H5、公众号、小程序等，直接执行。
2. **页面规划文档**：有 `v5-page-planning` 产出的「平台」字段时照抄，除非它与用户本轮明确指令冲突。
3. **项目 `v5-profile.md`**：按页面类别读取 `mobile` / `desktop` 映射；同一项目允许两端并存，必须逐页匹配类别。
4. **来源证据**：根据 Figma 画板尺寸、已有路由容器、设备壳和渠道判断。375/390/414 手机画板、H5/公众号/小程序壳通常为 mobile；1440 桌面画板、管理后台壳通常为 desktop。
5. **业务承载方式**：移动触达、即时查看、轻量输入与现场操作默认 mobile；密集表格、批量管理、复杂配置与多栏工作台默认 desktop。

**只有证据冲突**且会改变主结构时才询问用户。判定后立即把「页面/页面类别、平台、证据」回填 `v5-profile.md`；后续继续按映射执行。完整判定矩阵见 `references/08-platform-routing.md`。

硬规则：
- **移动页 = copy `assets/shell-mobile/`（A-m/B-m/C-m，类名 `v5m-`）**；桌面页 = copy `assets/shell/`（A/B/C，类名 `v5-`）。两套壳层都是稳定层，**同样禁止重画**。
- **禁止**把桌面壳层塞进 375 视口交差（80px 侧导航 + 920 列在移动端即违规）；**禁止**给移动页临场自创壳层；**禁止**因为「需求听起来像 App」就自行改判平台。
- 移动端没有右侧抽屉：桌面 C 的场景在移动端一律走 C-m 底部弹层。管理后台类页面默认 desktop，即便项目用户端是移动。
- 同一项目两个平台**共用同一份 `theme.css` / `DESIGN.md`**（颜色/圆角/字号令牌两端生效），风格不因平台分叉。
- 交付前必须运行 `scripts/check-platform.py`；任何跨端壳层混用都视为失败。

## 项目档案（持久化：风格 / 导航 / 壳层稳定复用）

技能是**通用标准**（base），项目的**风格 / 导航 / 壳层选择**存在**项目里**，技能每次自动读它套用，跨会话稳定，不再重述。

**约定位置**：项目原型目录（本工作区约定 `06_设计文件/原型/`；若不同则用该项目实际原型输出目录）。建档件：
- `v5-profile.md` — 项目身份：产品变量 + 各页类型用哪个壳层 + 指向下面文件。
- `DESIGN.md` — **UI 设计语言真源（人可读）**：色/字/标题阶梯/间距圆角阴影的语言与理由 + **§8 令牌之外**（CSS 表达不了的：标题阶梯/状态/角色/组件范式/动效/纪律）+ **§9 令牌契约**（机器源，= theme.css 的 `:root`）。
- `theme.css` — 项目风格层：**base + 覆盖**，只写改掉的令牌，引在 `tokens.css` 之后。空 = 沿用 V5 base。**内容应与 DESIGN.md §9 契约逐条一致**。
- `check-design.py` — DESIGN.md §9 契约 ⟷ theme.css 一致性校验：`--check` 报①漏实现/②野令牌/③值漂移（任一存在退出码 1）。
- `_nav.html` — 项目导航**单一来源（母版）**；各页 `<nav class="v5-nav">…</nav>` 是它的拷贝（静态 file:// 无法真 include）。换导航只改母版。
- `sync-nav.py` — 导航回灌器：把母版同步到所有 `页面-*.html` 并按页设高亮。`--check` 只检测漂移（有则退出码 1），无参则回灌。
- `_viewport-fit.js` — **桌面 1440 宽度适配引擎**（稳定层，copy 后勿改）：保持 1440 设计坐标，按 `viewportWidth / 1440` 等比缩放整张产品画布；移动 `v5m-` 页面自动跳过。
- `sync-viewport-fit.py` — 桌面适配注入器：给桌面 `页面-*.html` 注入 `_viewport-fit.js`，移动页不注入；`--check` 报缺失或平台误用（退出码 1）。
- `_pagenav.js` — **全站走查导航器·通用引擎**（稳定层，copy 后勿改）：左上角浮动列表 → 弹出全站页面清单（关系分组·当前页高亮·点击跳转），是原型侧走查的**唯一**手段。
- `_pagenav.pages.js` — 走查清单·**项目数据**（可变层）：`window.PGNAV_GROUPS` 定义分组与页面，把同一业务/Agent/流程的页面聚成一组。
- `sync-pagenav.py` — 走查导航注入器：把 `_pagenav.pages.js`+`_pagenav.js` 两行注入所有 `页面-*.html`（幂等，pages 在前）。`--check` 报缺引用（退出码 1）；缺 `_pagenav.pages.js` 时脚手架起始清单待重分组。

> **UX 层 vs UI 层**：v5-ux-rule 管 UX/结构/交互（壳层/组件/references）；`DESIGN.md`+`theme.css` 管 UI/视觉（设计语言）。两层解耦：换视觉不动结构。

**每次使用技能的开头先做**：
- 项目原型目录**已有** `v5-profile.md` → 读取并套用其风格 / 导航 / 壳层选择，**跳过对应确认**，直接进工作流。
- **没有** → **进入「首次建档引导」（交互式，见下节）**。不要静默建档：要一步步问用户、收集所需内容，再建。

## 首次建档引导（onboarding · 交互式 · 仅首次）

> 触发：调用本技能且项目原型目录无 `v5-profile.md`。**用户负责"说什么/给什么/选哪个"，agent 负责读、译、填、改、校验。** 全程不让用户手写文件。逐步走：

1. **产品身份**：先读项目上下文（PRD / `06_设计文件/页面规划/` / 已有页面）自动带出产品名、角色、业务对象；**向用户确认或补全**，只问缺的。
2. **页面来源**：检查有无 `v5-page-planning` 的页面规划文档。**有** → 规划驱动（版式以文档为准）。**无** → 提示"建议先跑 `/v5-page-planning`，或继续按规范驱动自行判断版式"，由用户定。
2.5 **平台映射**：问用户本项目哪些页面类别是移动端 H5、哪些是桌面端（如"用户端全部移动、管理后台桌面"），写入 `v5-profile.md` 的「平台映射」。规划文档已带「平台」字段的可直接汇总后请用户确认。
3. **导航项**：问用户左侧导航有哪些项、默认高亮哪个 → agent 据此改 `_nav.html`（用户只说，不写文件）。
4. **UI 设计语言路线**：用 `AskUserQuestion` 让用户三选一，并据选项**向用户索要对应输入**：
   - **A 沿用 V5 base**（默认）：无需输入；`DESIGN.md`/`theme.css` 留空。
   - **B 从 Figma 剥离（路线甲·皮肤级）**：请用户提供 **Figma 文件 key/链接 + 目标节点**，并提醒"开 Dev Mode、把目标画板设为当前活动页签"。→ agent 按 `references/06-figma-extract.md` 用 Figma MCP 提取，填 `DESIGN.md`（§1–6 理由 + §8 令牌之外 + §9 契约）+ 同步 `theme.css`。
   - **C 有现成设计规范（.md/文档）**：请用户提供**规范文件路径**。→ agent 读并翻译：色/字→§9 契约 + theme.css；"不可出现/状态/角色/组件"等→§8 令牌之外；理由→§1–6。
   - （**整套结构都不同** → 不走本技能皮肤覆盖，改用 figma-prototype-system；提示用户后退出本流程。）
5. **壳层选择**：规划驱动→采用各页规划文档版式；规范驱动→按页类型与用户确认（桌面 A 门户 / B 对话流 / C 抽屉；移动 A-m 门户 / B-m 对话流 / C-m 底部弹层）。
6. **建档执行**（agent 做）：从 `assets/project-profile/` copy 建档件（含桌面适配 `_viewport-fit.js`/`sync-viewport-fit.py` 和走查导航器 `_pagenav.js`/`_pagenav.pages.js`/`sync-pagenav.py`）→ 用收集到的信息填 `v5-profile.md` / `_nav.html`；按路线填或留空 `DESIGN.md`+`theme.css`；跑 `check-design.py --check`。有页面后分别运行两个注入器，走查清单再由 `sync-pagenav.py` 脚手架并人工重分组。
7. **回执确认**：把建好的档案小结（产品变量 / 导航 / 路线 / 壳层 / 校验结果）给用户审，确认后进工作流逐页画。

> 规则速记：**值**在 §9 契约 + theme.css；**理由/规则/令牌兜不住的**在 §8；两者由 `check-design.py` 机器校验一致。结构换不出来的（如"主按钮用品牌蓝"）按 §8 改对应组件。

**项目工具维护（技能自行判断是否回灌）**：凡是**改了 `_nav.html` 母版、或新增/改了任何 `页面-*.html`**，结束前跑 `python3 sync-nav.py --check`；若报漂移（退出码 1）就跑 `python3 sync-nav.py` 回灌，使全站导航与母版一致。新页面的高亮项按需在 `sync-nav.py` 的 `ACTIVE_MAP` 登记。新增/修改页面时还必须跑 `python3 sync-viewport-fit.py --check`（桌面页缺引用则运行无参数命令注入，移动页自动跳过）和 `python3 sync-pagenav.py --check`（缺走查导航引用则注入），并把新页面补进 `_pagenav.pages.js` 的对应分组。

> 引入顺序固定：`tokens.css`（base，不改）→ `theme.css`（项目覆盖）。页面两条 `<link>` 都要有，即便 theme 暂空。

## 工作流（每次定制时执行）

1. **读项目上下文**：PRD、已有页面、页面目录（标准产品定位见下「产品身份」）；**先按上节处理项目档案（有则读套用；无则走「首次建档引导」交互式建档）**；**若为规划驱动，再读对应页面规划文档**。
2. **提取本项目变量**：产品名、角色、业务对象——优先取 `v5-profile.md`，缺的才向用户确认**定制部分**，确认后回填档案。
3. **定平台 + 确定页面原型**：先按上面「平台判定」定 mobile/desktop；再定原型（桌面 A/B/C · 移动 A-m/B-m/C-m）——**档案已指定该页壳层**＝直接用；否则**规划驱动**＝采用规划文档版式字段、**规范驱动**＝按 `references/00-page-archetypes.md` 决策树判断。都**不自创新原型**。
4. **copy 稳定层 + 叠项目风格**：copy `assets/tokens.css`（base，不改）+ 对应壳层（桌面 `assets/shell/*.html` / 移动 `assets/shell-mobile/*.html`；**B 版式对话流优先 copy `assets/examples/chat-flow-full.html` / `chat-flow-execution.html` 成品样例页**，连同 `assets/icons/`、`assets/media/` 素材目录一起 copy 到项目原型目录），页面同时引项目 `theme.css`；桌面页导航填项目 `_nav.html`（移动页无侧导航，A-m 改 TabBar 项）。**禁止重画；图标/头像/插画一律用 `icons/`、`media/` 真实素材，禁止手绘 SVG 近似、禁止灰圆圈占位头像。**
   - **统一首页群像铁律（A / A-m）**：所有 V5 首页统一使用 `assets/media/home-agent-cast.png`，禁止替换、重画、裁成多张人物图或按项目 Agent 数量重新拼群像。桌面保持图片完整宽高比并居中展示；移动端按内容宽度等比缩放。该图是首页固定品牌群像，不承担 Agent 数量或身份映射；专员 chip、顶栏、消息头和过程插画仍按项目 `v5-profile.md` 的「Agent 固定形象映射」复用各自素材，一旦分配不得在后续页面或状态中换人。
   - **首页输入台 Agent 跳转铁律**：首页输入台里的每个 Agent / 专员 chip 都必须是可点击真实链接，直接进入该 Agent 对应的 B / B-m 对话页，或以对话为基座的 C / C-m 首态；禁止跳到功能列表、案例选择、管理配置、介绍页等非对话页面。目标对话页不存在时，先补对应对话入口，再挂链接。首页下方普通功能入口卡不受此限制，可进入功能页。
   - **首页入口标题铁律**：首页快捷入口卡的标题使用统一字号和字重，禁止把标题首字、首字母、emoji 或装饰符单独放大；标题直接完整显示业务名称。
4.4 **桌面宽度适配铁律**：桌面 A / B / C 统一保留 `1440px` 设计坐标，实际显示比例固定为 `scale = viewportWidth / 1440`。必须 copy `_viewport-fit.js` 并运行 `python3 sync-viewport-fit.py` 注入所有桌面 `页面-*.html`；**不按高度二次缩放**、不为 1024/1366/1920 另造断点、不单独改字号或组件宽度。适配引擎按当前屏幕高度补足设计画布，长内容仍可纵向滚动；评审 `_pagenav.js` 按钮位于缩放画布外，保持屏幕像素大小和可拖动手感。移动 A-m / B-m / C-m 不接入该引擎，仍使用 375 专属壳层。
4.5 **对话流标准件铁律（每次一模一样）**：输入台、消息头、用户气泡、拍了拍、完成操作栏、追问建议这六个标准件，**必须整块 copy 样例页对应 HTML+CSS，只允许替换业务文案**——不重写类名、不调间距字号颜色圆角、不换图标。产出后这六件与 `examples/chat-flow-full.html` 逐像素一致是验收项；任何"按理解微调"都算违规。`components/` 下同名组件已与样例页对齐（同一规格、类名兼容），copy 到哪份都一样。
4.6 **历史对话轨道铁律（V5 History Rail）**：桌面端 B / C 标准对话页必须整块 copy `assets/components/history-rail.html` 的 `.v5-history-rail` 结构、样式和初始化器。默认显示右缘 16 条消息刻度，hover / focus 展开 300×244 历史弹层；初始化器仅接受 `?conversation=01..16`，并同步唯一当前行、当前刻度和 `aria-current`。带抽屉时锚定主对话列右缘、位于抽屉左侧。不得同时保留顶部历史按钮，不得改成常驻历史侧栏或普通下拉菜单。模态遮罩出现时隐藏且禁止聚焦：仅对当前可见遮罩生效，轨道和链接全部移出 Tab 顺序，遮罩关闭后恢复。移动端不套用该桌面组件。
5. **复用基础组件**填中间内容槽位：从 `assets/components/*.html` 取，只填业务内容；遵循「一页一态、可独立打开截图」。
6. **套交互/文案/AI 规则**：见 `references/03–05`。
6.5 **接跳转 + 挂走查导航器**：
   - **全站走查用浮动导航器**（不是往页面塞演示按钮）：copy `_pagenav.js`（引擎，勿改）+ 填 `_pagenav.pages.js`（按业务/Agent 关系分组的页面清单）→ 跑 `python3 sync-pagenav.py` 注入所有页面。默认左上角一个列表 icon 即可跳转任意页，**按钮可拖到页面任意位置**（拖拽 vs 点击自动判定，位置存 `localStorage` 跨页面/刷新保留，仅本机走查用），天然不污染真实页面（产品身份·真实内容原则）。
   - **页面内真实跳转**：按规划文档的「页面跳转关系 / 区域『出链 →』」，把**真实产品里本就存在**的触发点（导航项 / CTA 按钮 / 真实卡片 / `@`chip）渲染成相对链接 `<a href="页面-NN-…html">`。终点须真实存在；无目标的元素不强加链接。首页输入台 Agent chip 的终点只能是对应对话页，不能是功能页。**严禁为了走查凭空新增「查看功能演示」「进入XX对话」等演示/导览按钮**（违反真实内容原则）——跳转是给真实入口挂真实去向，全站遍历交给导航器。
7. **同步自检**：改了 `_nav.html`/页面 → `python3 sync-nav.py --check`（漂移则回灌）；新增/改了页面 → `python3 sync-viewport-fit.py --check` + `python3 sync-pagenav.py --check`；改了 `DESIGN.md`/`theme.css` → `python3 check-design.py --check`（①漏实现/②野令牌/③值漂移则修到一致）。
8. **截图自检**：对照 `references/99-review-checklist.md`，并与 `assets/figma-reference/*.png` 基准图比对。

## 产品身份（不可变约束）

- **产品**：大明白 V5，面向大学教师的 AI 教学工作入口。
- **用户/角色**：高校老师、教学中心配置人员、交互评审者；核心 Agent = V5 小管家、课代表 Agent、普通 Agent。
- **气质**：专业、克制、清晰，像可信赖的教育 SaaS 工作台。
- **反例**：不做营销页/装饰型 AI 落地页/炫技视觉；不把 PRD、路由名、评审备注混入用户可见区；避免无意义图标、夸张渐变、低对比灰字、重装饰卡片堆叠。
- **真实内容原则（硬约束，重要）**：**始终站在真实用户视角画页面**——页面上的每个字、每个按钮、每个入口，都必须是**产品上线后终端用户真会看到、真会用**的东西。**严禁把「原型/演示/导览」类脚手架混入真实页面**，典型违规：
  - 演示/导览入口：「查看功能演示」「立即体验」「看看怎么用」；
  - 页面自指入口：在「学业规划助手」页里放「进入学业规划助手对话」按钮——用户**已在该功能内**，不需要"进入"，也不需要"看演示"；
  - 把介绍页 / 落地页式的营销、导览内容当成功能页来画。

  判据一句话：**"上线后，真实用户在这个页面会看到这句话 / 这个按钮吗？"** ——答案是"不会"，就删掉，或换成真实产品里该有的语义。走查所需的页面跳转只复用**真实可点击元素**（导航项、真实卡片/入口），**不得为走查新增假的演示/导览按钮**（见工作流 6.5）。
- **无障碍**：正文 WCAG AA 对比度；清晰焦点与足够触达；不靠颜色单独表达状态；动效仅轻量反馈并尊重 reduced motion。

## 与自由美化类技能的协作边界

- `v5-ux-rule` 管的项目要求**跨页视觉一致**（同一套 tokens/组件在所有页面复用）；`frontend-design`、`impeccable` 等技能默认倾向**为单个界面挑一个大胆/独立的美学方向**，两者的默认取向天然冲突。
- 当用户在 `v5-ux-rule` 已建档的项目里，对某一页/某个组件发起"美化""重新设计视觉""换个风格"这类请求时，**先用 `AskUserQuestion` 确认作用域**，不要默认套用自由美化技能的独立风格倾向：
  - 选项一般是「体系内精修」（不引入新字体/新配色，只在现有 tokens/组件基础上打磨细节，且事后要考虑是否回收进公共组件库）vs「独立视觉探索」（不受当前项目 token 约束，明确只影响这一页/这一处，且探索结果默认**不**自动推广到其它页面）。
  - 选了「独立视觉探索」也不能静默替换公共组件（如 `v5-rcard`）——要么另起专用 class，要么明确询问是否要固化为新的项目级选择并记录进 `v5-profile.md`。
  - 用户事后要求"回滚"这类探索时，直接恢复到探索前的公共组件版本，不要保留混合状态。

### `assets/`（稳定层，直接 copy）
- `tokens.css` — 设计令牌（颜色/字号/间距/圆角/阴影/布局尺寸；含移动端 `--v5m-*` 布局段）
- `shell/home-portal.html` (A) · `shell/chat-flow.html` (B) · `shell/drawer.html` (C·1/3屏 500) · `shell/drawer-half.html` (C·半屏 720)
- `shell-mobile/portal.html` (A-m·TabBar 门户) · `shell-mobile/chat-flow.html` (B-m·移动对话流) · `shell-mobile/sheet.html` (C-m·底部弹层，`--half`/`--action` 变体) — H5 375×812，类名前缀 `v5m-`
- `components-mobile/mobile-ui.css` — 当前移动端公共结构与组件样式；59px 原型状态区、44px 顶栏、343px 输入台、底部弹层、任务/文件/追问/历史组件统一从这里复用。
- `examples-mobile/` — **移动端成品样例页**：A-m 门户，以及 B-m/C-m 的对话、输入、任务、思考、智能体/技能、反馈、文件、追问、历史。新移动页优先 copy 对应成品样例，不从桌面样例缩放。
- `components/` — dialog · card · chat-result-card（对话流结果卡/列表项，B 版式专用，见下）· history-rail（桌面 B / C 标准对话页历史轨道）· button · form · table · pagination · toast · empty-state · input-composer · file-upload
- `examples/` — **成品样例页（copy 真源，优先级高于 shell/*.html 骨架）**：`chat-flow-full.html`（B·全生命周期展开态：过程卡+插画+拍了拍+最终回答+操作栏+追问建议+V5 History Rail，Figma 2117:1928）· `chat-flow-execution.html`（B+C·执行中：执行计划抽屉+运行日志时间线+任务总数浮层+并行 Agent 胶囊+气泡 hover 操作，Figma 2907:2110）· `chat-flow-plan-edit.html`（C·执行计划编辑态：警示条+已暂停+取消/保存+可编辑节点+替换/删除，Figma 2907:3279）· `home-portal-full.html`（A·门户：大标题星饰+统一 `home-agent-cast.png` 首页群像+920 输入台含专员 chip+待办建议卡，Figma 823:1390）。copy 样例页时必须连同 `icons/`、`media/` 一起。
- `icons/` — **真实图标库**（从 base Figma 导出的 SVG，语义命名：nav-*/topbar-*/composer-*/action-*/msg-*/status-* 等）。**对话流/壳层页面的图标一律取自这里，禁止手绘 `<path>` 近似**；缺的图标先回 Figma 导出补库，再用。
- `media/` — **真实形象素材**（PNG）：`home-agent-cast.png`（所有 A / A-m 首页唯一群像，1142×380 透明底，禁止替换或拆分）· `logo-v5` · `agent-xiaoguanjia` + `agent-portrait-a/b/c/d`（头像 / 专员 chip）· `illustration-desk-1/2/3` + `illustration-office-*`（过程卡右缘"数字员工"插画 178×120，共 15 张，每 Agent 选一张专属）· `portal-hero-1..5` / `expert-avatar`（旧素材，仅作追溯）· `model-logo` · `topbar-xiaoguanjia` · `user-avatar`。对话内 Agent 素材必须由 `v5-profile.md` 固定映射并跨页面复用，禁止灰圆圈占位或临时换图。
- `avatars/` — **形象备选库**（Figma「头像-UI」页实测导出，35 个 208×208 头像：主IP `zhu-1..4` · 女 `nv-1..15` · 男 `nan-1..6` · 历史人物 `kongzi/libai/dufu/liqingzhao/daerwen/dafenqi/dikaer/fangao/fuluoyide/weida`）。**选用铁律：原型里任何 Agent/角色需要头像时，一律从本库挑选（打开 `avatars/_catalog.html` 目录页比对气质选形象），学科类 Agent 优先用对应历史人物（如数学→韦达/笛卡尔、语文→李白/杜甫/李清照、美术→梵高/达芬奇、生物→达尔文、心理→弗洛伊德、国学→孔子）；禁止用库外图片、生成图或占位圈。** 头像配专属底色（柔和色 `#7b859f/#979f7b/#927b9f/#b16aba/#ffb84d/#6fb7e9/#4e9e96` 系）。
- `figma-reference/*.png` — 各页/组件的 Figma 基准截图（视觉参考 + 自检比对，不抄业务文案）
- `project-profile/` — **建档模板**（首次使用时 copy 到项目）：`v5-profile.md` · `DESIGN.md`（UI 设计语言，含 §8 令牌之外 + §9 契约）· `theme.css`（空覆盖骨架）· `check-design.py`（DESIGN⟷theme 校验）· `_nav.html` · `sync-nav.py`（导航回灌器）· `_viewport-fit.js`（桌面 1440 宽度适配引擎）· `sync-viewport-fit.py`（桌面适配注入器）· `_pagenav.js`（可拖动走查导航器引擎）· `_pagenav.pages.js`（走查清单数据模板）· `sync-pagenav.py`（走查导航注入器）

### `references/`（可变层，判断依据）
- `00-page-archetypes.md` — 页面原型决策树 + 每种固定结构与槽位
- `01-tokens.md` — 令牌取值表 + 用法（禁裸值）
- `02-page-shell.md` — 壳层尺寸/栅格/复用纪律（一页一态等）
- `03-components.md` — 各组件标准用法（弹窗居中/宽度、按钮两种主行动等）
- `04-interaction-copy.md` — CRUD/确认取消/三态/文案语气
- `05-ai-patterns.md` — 对话生命周期、AI 卡片排布、文件上传状态机、`@`/`+`
- `06-figma-extract.md` — 从项目自有 Figma 剥离设计语言（路线甲）→ 填 DESIGN.md + 映射 theme.css
- `07-card-anatomy.md` — **卡片设计规范**：对话流卡片统一解剖（类别标签→标题→内容块/选项→操作行）、五种参考形态、状态 chip/日期行；真源代码在 `components/chat-result-card.html`
- `08-platform-routing.md` — 逐页平台判定优先级、证据矩阵、混合项目映射与冲突处理。
- `09-mobile-ui.md` — 当前移动端几何、壳层、组件、状态和 Figma 节点真源。
- `99-review-checklist.md` — 交付前自检清单

## 视觉标准

**base 视觉标准（桌面）** = Figma「全自动课程助教 V5」文件（`4t35fBc4I64igQH6qZpIGL`）。`assets/` 由其提取/对齐；标「派生」的件（table/pagination/toast/empty-state、半屏抽屉、对话中文件 chip）= Figma 无设计、按 V5 令牌补充。修改 base 资产时以此 Figma 为准。

**base 视觉与结构标准（移动 B-m/C-m）** = Figma「全自动课程助教 V5」文件（`4t35fBc4I64igQH6qZpIGL`，画布 `6050:5423`）。对话、输入、任务、思考、智能体/技能、反馈、文件、追问、历史和底部弹层均以该画布为当前真源。移动门户 A-m 在此画布尚无对应页面，暂沿用 Figma「大平台设计-UI」教师端 app（`ljg4eVP3elzzx5b2Q8FYdI`，画布 `56301:10134`）的门户结构，但颜色、字体和业务内容仍走 V5 base 与项目 `theme.css`。

**项目视觉标准**：若项目走了「Figma 剥离」（路线甲），该项目的视觉真源是其 `DESIGN.md`（源自项目自有 Figma），通过 `theme.css` 覆盖 base —— 此时项目自检以 DESIGN.md/项目 Figma 为准，结构仍遵循 base 壳层。
