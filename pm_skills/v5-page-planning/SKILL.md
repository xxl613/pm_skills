---
name: v5-page-planning
description: Use when turning a structured requirement/parameter list (each item with an ID, like 大明白 V5 需求池) into a set of per-page planning docs BEFORE drawing prototypes. Produces a page map with a parameter-coverage matrix plus one planning doc per page (版式/design goal/low-fi wireframe/区域×内容/covered parameter IDs). Output fields align to v5-ux-rule so prototype drawing becomes fill-in, not re-derivation. Trigger words：页面规划、需求拆页、把需求拆成页面、页面地图、参数覆盖矩阵、需求转页面、requirements to page plan. NOT for drawing hi-fi prototypes (that is v5-ux-rule) and not for requirement triage/scheduling.
---

# V5 Page Planning

把**结构化需求参数清单**拆成**可追溯的页面规划文档集**，坐在流水线第一段：

```
需求参数清单 →【v5-page-planning（本技能，只规划不画）】→ 页面规划文档集 →【v5-ux-rule】→ 原型
```

**只规划，不画原型。** 高保真原型归 `v5-ux-rule`；本技能产出低保真线框 + 结构化规划，让 PM 先确认版式与信息结构，再交给下游。

## 输入

结构化需求/参数清单，每条带 `ID + 摘要 + 关联模块`（如 `01_产品设计/V5需求池.md` 的登记表）。散文式 PRD 非主输入。

## 产物（一个目录）

默认落 `06_设计文件/page-plans/<日期>-<项目名>/`：
- `_页面地图.md` — 由 `assets/page-map-template.md` 生成：页面清单 + **参数覆盖矩阵**。
- 每页三件套（同名）：
  - `页面-NN-<slug>.md` — 规划文档，由 `assets/page-plan-template.md` 生成。
  - `页面-NN-<slug>.wireframe.html` — 低保真线框 HTML 源。
  - `页面-NN-<slug>.layout.png` — 由线框渲染的预览图（内嵌进 .md）。

## 工作流（4 步，第 2 步是确认闸）

1. **归一化输入**：读需求清单，抽成原子参数表 `[ID, 摘要, 关联模块]`。
2. **聚类成页 + 提案（闸口，硬性停轮）**：按"用户在哪一步、同屏完成什么"把参数聚成若干页面；
   先用 `assets/page-map-template.md` 产出**页面地图提案**（含页面清单 + 参数覆盖矩阵 + **「页面跳转关系」边表 + 流转简图**）给用户确认（改/合/拆），
   **得到确认前不批量生成单页文档**。跳转关系即用户流，左导航作为全局边单列一次。
   - **确认对象是页面地图本身，不是拆分问题的答案**：若用 AskUserQuestion 问了粒度/范围类问题，答案只用于**修订地图**；修订后必须把**新版页面清单**再次给用户过目，等到「确认 / 可以 / 开始生成」这类对地图的明确放行才进第 3 步。
   - **提案与生成不同轮**：产出或修订页面地图的那一轮到此结束（stop），不得在同一轮里接着生成单页文档——哪怕改动看起来只是"按用户答案机械调整"。
   - 例外仅一种：用户**当轮明说**"地图不用再看，直接生成"。
3. **逐页生成**：用户确认后，每页 copy `assets/page-plan-template.md`：
   - 用 `references/page-archetype-cheatsheet.md` 先定**平台**（mobile/desktop，取项目 `v5-profile.md` 平台映射或用户交代，缺则问一次；写进「平台」字段）再选**版式**（桌面 A/B/C+宽度 · 移动 A-m/B-m/C-m，禁自创新版式）。
   - **布局产出两个同名兄弟文件**（与该页 .md 同目录）：
     - `页面-NN-<slug>.wireframe.html` ← copy `assets/wireframe-snippets/` 对应版式起手式，改区域文字标注（区域名 · 承载内容 · 参数ID）。这是布局 HTML 的唯一来源。
       - **功能展示 / 演示类页面（B 对话流 demo）必须写出完整对话文字**：用户问句原文 + 助手分轮回答 + 结果卡内真实文案（标题 / 字段 / 数值示例），按对话生命周期逐轮铺开（用户请求 → 主Agent 判断/派发 → 场景Agent 生成 → 产物 → 完成句 → 后续建议）。**禁止用「返回结果卡 ×N」「能力清单」等抽象占位顶替对话内容**；低保真只约束视觉（虚线框、无成品皮肤），对话文字必须是可评审的真句子。同时在 .md 填「对话脚本」段（见模板）。
     - `页面-NN-<slug>.layout.png` ← 渲染上面 html：`bash assets/render-wireframe.sh 页面-NN-<slug>.wireframe.html 页面-NN-<slug>.layout.png`。
     - 在 .md 的「布局线框」段**内嵌该 PNG** + 链接 .wireframe.html 源（改 html 后重跑脚本刷新图，避免图文漂移）。
   - 填"区域 × 内容"，组件名引用 v5-ux-rule `assets/components/*`（card/form/table/input-composer/…）。
   - 填"满足的参数清单"。
   - 填"区域 × 内容"时同时填**「出链 →」列**：该区域可点击元素跳去哪页（须是地图里登记、真实存在的页）。
4. **覆盖自检**：回填 `_页面地图.md` 的参数覆盖矩阵；显式标出
   **❌漏接**（无任何页面承接）与 **⚠️重复**（多页承接待确认）。漏接必须解决后才算完成。
   并做**🔗 入口/出口自检**：每页 ≥1 入边（非孤岛）、≥1 出边或明确终点；跳转终点真实存在（断链=失败）。

## 与 v5-ux-rule 的交接契约（每页字段刻意对齐其输入）

| 本技能字段 | 下游 v5-ux-rule 用途 |
|---|---|
| 平台（mobile/desktop） | 平台判定第二来源（第一来源是项目 `v5-profile.md` 平台映射），下游照抄不改判 |
| 版式（桌面 A/B/C+宽度 · 移动 A-m/B-m/C-m） | 直接选壳层 `shell/home-portal`/`chat-flow`/`drawer`/`drawer-half` 或 `shell-mobile/portal`/`chat-flow`/`sheet` |
| 区域 × 内容（引用组件名） | 填 `assets/components/*` 槽位 |
| 设计目标 | 气质/取舍判断 |
| 满足的参数清单 | 贯穿原型自检，确保覆盖需求 |
| 页面跳转关系 / 区域「出链 →」 | 把触发点渲染成 `<a href="页面-NN-…html">`，让原型可点击走查（file:// 相对链接） |

## 纪律

- **先地图后单页，且中间必须隔一次用户放行**：任何一版页面地图（首版或修订版）展示给用户之前/之时，都不算已确认；把"用户回答了我的提问"当成"地图已确认"是本技能的已知违规模式（2026-07-06 守望云心会话实证）。
- **不自创新版式**（桌面 3 + 移动 3 之外没有）；列表/详情/状态页不是独立页面（见 cheatsheet）。**平台不临场猜**：每页「平台」字段必填且有来源。
- 线框保持**低保真**（虚线框 + 标签），不画成品皮肤——皮肤是 v5-ux-rule 的活。
- **演示页写真话**：凡「展示功能 / 演示能力」的页面，线框与规划文档里的对话必须是完整、具体的真实文字（含助手回答与结果卡文案），而非占位标签——低保真指视觉风格，不指内容含糊。
- **禁止一问多卡**：一个用户问题只能对应一次助手回合、展示与该问题直接相关的结果（通常 1 张结果卡）；页面若要呈现多个环节/维度，必须拆成用户逐轮追问、一轮对应一张卡，不能让用户问一句就把后续所有环节的卡一次性甩出来。自检时数一下"用户提问次数"是否 ≈"结果卡数量"，明显少于就是没拆够。
- **B 对话流左导航与 A 首页/门户逐字一致**（同一套导航项 + 当前激活项），不各写一套；对话框（输入台）钉在底部。
- tokens/组件/决策树**引用 v5-ux-rule，不复制重写**，避免两份规则漂移。
- 每个参数 ID 必须在覆盖矩阵出现一行；漏接是规划失败。
- **跳转真实可达**：页面地图/出链里写的每条边，终点必须是页面集里真实存在的页（同参数一样，断链=规划失败）；跳转是**规划**产物（边表+href 目标），视觉仍归 v5-ux-rule。

## 资产索引

- `assets/page-map-template.md` — 总览 + 覆盖矩阵模板
- `assets/page-plan-template.md` — 单页模板
- `assets/wireframe-snippets/{A-home-portal,B-chat-flow,C-drawer,C-drawer-half}.html` — 桌面四版式低保真线框
- `assets/wireframe-snippets/{Am-mobile-portal,Bm-mobile-chat-flow,Cm-mobile-sheet}.html` — 移动三版式低保真线框（375）
- `assets/render-wireframe.sh` — 线框 HTML → PNG 渲染（Chrome headless，零安装）
- `references/page-archetype-cheatsheet.md` — 版式速查（引用 v5-ux-rule 决策树）
