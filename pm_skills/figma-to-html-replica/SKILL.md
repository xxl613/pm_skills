---
name: figma-to-html-replica
description: >-
  将 Figma 画板高保真复刻为 HTML/CSS（或项目栈），并通过截图对比迭代缩小视觉差异。
  触发词：「Figma 转 HTML」「复刻 Figma」「画板还原成页面」「Figma 高保真落地」
  「截图对比 Figma」「对齐设计稿 HTML」。
---

# Figma → HTML 高保真复刻 Skill

## 目标

在**可控迭代次数**内，把指定 Figma 画板还原为可运行的前端页面，并用**截图对比**验证与设计的差异，逐轮修正。

**默认验收口径**：以 **1:1 视觉复刻** 为目标。除非用户明确放宽要求，否则**不接受**用占位色块、临时几何图形、伪 icon、emoji 或“先这样”的替代方案冒充设计稿中的真实可见资产。

---

## 前置条件

| 条件 | 说明 |
|:---|:---|
| Figma 访问 | 已配置 Figma MCP / 插件，能调用 `get_design_context`、`get_screenshot`、`get_metadata` |
| 目标栈 | 默认 **静态 HTML + CSS**；若仓库为 React/Vue/Vite，则复刻为对应组件，本 skill 的流程不变 |
| 设计依据 | 优先以 **DESIGN.md / 设计 Token**（若项目有）约束颜色、圆角、字号；无则完全以 Figma 导出为准 |
| 截图工具 | **默认使用 Chrome 插件只读截图或独立无头 Chrome**；需要当前登录态时再使用用户 Chrome 会话；Playwright / Puppeteer 作为备选 |

## 工作流（三阶段 + 迭代环）

### 阶段 1 — 整板复刻（一次交付）

1. **锁定范围**
   - 记录：`fileKey`、`nodeId`（画板 Frame）、画板尺寸（宽×高，如 1440×900）。
   - 若 URL 为 `node-id=11452-3953`，转换为 API 形式 `11452:3953`。

2. **拉取设计信息**
   - 使用 `get_metadata` 理清层级（侧边栏 / 顶栏 / 主内容 / 输入区等）。
   - 使用 `get_design_context` 获取结构提示与 MCP 给出的**临时资产 URL**（仅作下载来源）；**禁止**凭记忆编造色值与尺寸。
   - 建立「可见资产清单」：逐项记录设计稿中出现的原始图片、SVG、mask、徽标、icon、头像、插画、纹理和装饰图形。后续实现必须逐项落地，不能只复刻外框和文字。
   - 对复杂节点可配合 `get_screenshot` 作为视觉参照。

3. **实现页面**
   - **先结构后像素**：语义化区块 → Flex/Grid 布局 → 再调间距与字体。
   - **资产处理（强制本地化 + 格式校验）** — 详见下方「资产管理规范」。
   - **真实资产优先（强制）**：凡 Figma 中可见的 icon、插画、徽标、装饰图形、头像遮罩、按钮内图形，默认都应使用 **Figma 导出的真实本地资产** 或可证明等价的原生矢量/CSS 复现。**禁止**用纯色方块、渐变块、临时圆形、伪 SVG、emoji 等占位方式交付。
   - **坐标**：若设计为固定画板，关键区域可用 Figma 绝对坐标换算为 padding/margin（例如聊天区左右各 70px、内容宽 920px），避免整页只用 `max-width` 而与设计稿不一致。

4. **输出物**
   - 可访问的页面路径（如 `dist/index.html` 或 dev server URL）。
   - 简短说明：技术栈、入口文件、如何本地打开。
   - 若存在未复刻项，必须显式列出，不得在未说明的情况下以占位实现直接交付。

---

### 阶段 2 — 截图对比（每轮必做）

1. **Figma 侧**
   - 对同一 `nodeId` 调用 `get_screenshot`（或导出与浏览器同尺寸的 PNG）。
   - 保存为：`artifacts/figma-{nodeId}-{n}.png`（`n` 为迭代轮次）。

2. **HTML 侧**
   - 使用 Chrome 插件只读截图或独立无头 Chrome 截图。默认优先无头 Chrome，避免抢夺用户当前 Chrome 焦点；只有必须复用用户登录态、扩展态或当前标签页状态时，才使用用户 Chrome 会话。

   ```bash
   # 无头 Chrome（默认，无焦点）
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless=new \
     --disable-gpu \
     --hide-scrollbars \
     --window-size=<画板宽>,<画板高> \
     --screenshot=artifacts/html-{nodeId}-{n}.png \
     "<url>"

   # Playwright（备选，需先 npx playwright install chromium）
   npx playwright screenshot --viewport-size=1440,900 --wait-for-timeout=3000 <url> artifacts/html-{nodeId}-{n}.png
   ```

   - **视口宽度** = 画板宽度（如 1440），**deviceScaleFactor** 建议固定为 `1` 或 `2`，整轮流程保持不变。
   - 等待字体与图片加载完成（`networkidle` 或固定 `waitForTimeout` + 关键选择器出现）。
   - 如使用 Chrome 插件连接用户 Chrome，只做打开 URL、设置视口、等待加载、截图、读取 DOM / computed style 等只读检查；除非验证交互必需，不点击、不输入、不切换用户正在使用的标签页。

3. **差异分析**
   - **像素 diff**（可选）：使用 `pixelmatch` / `resemblejs` 等工具生成 diff 图，并输出**差异比例**。
   - **人工复核**：列出差异清单（区域 + 现象 + 可能原因），例如：
     - 顶栏高度少 2px；
     - 输入框圆角与设计不一致；
     - 字体导致文案折行多一行。

4. **通过标准（建议写入本轮结论）**
   - 像素 diff **差异比例 ≤ 5%**（约定阈值，团队可再收紧）；或
   - **无结构性问题**（不错位、不重叠、不少块），仅允许字体亚像素级差异。
   - **无资产缺失问题**：设计稿中可见的 icon / SVG / 插画 / 徽标若缺失、错用占位图形或类型错误，直接判定**未通过**，即使像素 diff 尚未超阈值。

**约束**：未完成至少一轮「Figma 截图 vs HTML 截图」对比前，不能宣称“已复刻完成”或“已 1:1 对齐”。

---

### 阶段 3 — 按差异修改 → 回到阶段 2

1. 根据阶段 2 的差异清单**逐项修改** HTML/CSS（或组件样式），避免无关重构。
2. 修改完成后**重新执行阶段 2**，轮次 `n + 1`。
3. **最多循环 5 轮**（含首轮对比）。超过仍不达标则：
   - 输出「剩余差异说明」与「建议」（如：需设计导出切图、需 Webfont、需设计改标注）。

**提前结束**：若某轮 diff 已低于阈值或差异清单为空，可**立即结束**，不必凑满 5 轮。

---

## 迭代环小结

```text
[1 整板复刻] → [2 双端截图 + 差异分析] → 未通过？
       ↑___________________________________|
                    [3 修改]（最多 5 轮）
```

---

## 资产管理规范（关键）

### 真实性规则（必须执行）

- 凡设计稿中**用户可见**的视觉资产，默认都属于交付范围，不能因为“先搭结构”而长期停留在占位状态。
- **禁止交付型占位**：纯 CSS 色块、渐变块、临时圆圈、伪 icon、emoji、随手手写 SVG path，如果它们只是为了“先看起来差不多”，都不算完成。
- 只有两种情况可以不落真实资产：
  1. 该元素本身就是用可读的原生 CSS/HTML 即可 **等价复现** 的简单几何图形；
  2. Figma/MCP 当前确实无法导出，且已在交付说明中**显式标注阻塞项**，等待用户或设计确认。

### 下载与本地化

- 凡图片、SVG、图标等**一律下载**到仓库内固定目录。
- **禁止**在交付代码中保留 `figma.com/api/mcp/asset/...` 链接——这些是临时 URL，过期后资源不可访问。
- Figma 中的原始图片素材必须随 HTML 交付复制到项目资产目录，并在代码中引用本地文件。不能只用 CSS 重画一个“看起来像”的替代品，除非已经证明该元素本身是简单几何图形且可等价复现。
- 如果 Figma 用图片作为 `maskImage`、alpha mask、裁剪遮罩或带颜色叠加的徽标，必须同时复刻「本地 mask 素材 + Figma 颜色/背景/裁剪方式」。不要直接把白色 mask 图当普通 `<img>` 使用，也不要丢掉 mask 只保留文字。
- 如果 MCP 返回的是整组品牌标识、徽标组合或按钮图形资产，应优先作为完整资产复刻；不要拆成临时文字和 CSS 图形，除非设计稿本身就是文本层和基础矢量层。

### 可迁移资产规则（HTML 需要能回流 Figma）

> 浏览器里看起来正确，不等于后续能稳定导入 Figma。关键视觉资产必须是 Figma 可识别、可编辑或可作为图片填充稳定呈现的真实资产。

- 对品牌 logo、校徽、头像、产品图标、功能图标、插画和纹理等关键资产，HTML 中优先使用真实 `<img>` / SVG 文件，不要只依赖 CSS `mask-image`、`background-image`、icon font、emoji 或浏览器合成效果。
- 如果原始资产是白色透明 PNG、alpha mask 或需要 CSS 叠色的图形，必须额外生成一份**捕获友好版本**：
  - 固定品牌色的 SVG / PNG；或
  - 已经合成好颜色和透明度的可见图片。
- 捕获友好版本必须满足：单独打开可见、放在白底/浅底上可见、无需 CSS mask 或背景叠色也能表达正确视觉。
- 原始资产和捕获友好资产都应登记在资产清单中。示例命名：`brand-mark-mask.png`、`brand-mark-red.svg`、`brand-mark-red.png`。
- 如果项目后续会执行 HTML → Figma，同一个关键资产不得只以 CSS mask 方式出现在最终页面；否则 Figma 捕获可能产生空白、纯色块、错误裁剪或不可见节点。
- 对必须保留动态换色能力的资产，优先用 SVG `currentColor` 或多份显式色值 SVG；不要把动态换色建立在 `mask-image` 上作为唯一实现。

### ⚠️ 格式校验（必须执行）

> **经验教训**：Figma MCP 导出的资产 URL 不携带文件后缀，下载时常以 `.png` 保存，但实际内容可能是 **SVG**。浏览器按 `image/png` MIME 加载 SVG 内容会导致**图标完全不显示**，且控制台不一定报错，极难排查。

下载完成后**立即**执行格式校验：

```bash
# 对所有 .png 文件检测真实格式
for f in <资产目录>/*.png; do
  if file "$f" | grep -q 'SVG'; then
    mv "$f" "${f%.png}.svg"
    echo "FIXED: $(basename $f) → .svg"
  fi
done
```

**规则**：文件后缀必须与实际内容格式一致（PNG→`.png`，SVG→`.svg`，JPEG→`.jpg`）。

### 资产引用方式（按项目栈选择）

| 项目类型 | 目录 | 引用方式 |
|:---|:---|:---|
| 静态 HTML | `public/assets/<功能名>/` | `<img src="/assets/功能名/icon.svg">` |
| Vite + React/Vue | `src/assets/<功能名>/` | 通过 `import` 语句（Vite 自动 bundle） |
| Webpack | `src/assets/<功能名>/` | 通过 `require()` 或 `import` |

### Vite 项目资产最佳实践

1. **资产放 `src/assets/` 而非 `public/`**：Vite 会对 `src/` 下的资产做 hash 命名、Tree-shaking、内联小文件等优化。

2. **创建资产清单文件** `src/assets/<功能名>/index.ts`：

   ```typescript
   import logo from './sidebar-logo.svg'
   import calendar from './nav-calendar.svg'
   import userAvatar from './user-avatar.png'
   // ... 所有资产

   export const assets = { logo, calendar, userAvatar /* ... */ } as const
   ```

   页面中统一导入：`import { assets as ASSETS } from '../assets/<功能名>'`

3. **TypeScript 声明文件**：若项目没有 `vite-env.d.ts`，需创建：

   ```typescript
   /// <reference types="vite/client" />
   ```

   否则 TS 不认识 `.png` / `.svg` 的 import 语句。

---

## 注意事项（减少假差异）

| 风险 | 应对 |
|:---|:---|
| 视口/DPR 不一致 | 固定 `viewport` 宽度与 `deviceScaleFactor`，全程不变 |
| 字体不一致 | 在 CSS 中显式声明 `font-family` 与 `font-weight`；若仍偏差，在报告中标注「字体限制」 |
| 动态文案 | 对比时使用固定假数据，关闭实时时间 |
| **资产格式错误** | **下载后立即用 `file` 命令校验**，将 SVG 内容的 `.png` 重命名为 `.svg`（见「资产管理规范」） |
| **用占位冒充真实资产** | 将“图标/插画/徽标缺失”视为失败项；优先补真实资产，再做像素微调 |
| **CSS mask / 白色透明 logo 回流 Figma 失真** | 为关键资产生成捕获友好 SVG/PNG，并在 HTML 中以真实 `<img>` / SVG 呈现 |
| 远程图未加载 | 资产已本地化后不存在此问题；截图前仍等待 `img` onLoad |
| Figma 资产过期 | **以本地化流程规避**：交付物中不得依赖 MCP 临时 URL |
| 截图工具安装失败 | 默认优先使用本机 Chrome 的 `--headless=new` 截图；如果 Chrome 插件或无头 Chrome 不可用，再退回 Playwright / Puppeteer，并在结论中说明 |

---

## Agent 执行检查清单（每轮可勾选）

- [ ] 已记录 `fileKey`、`nodeId`、画板尺寸
- [ ] 已用 `get_design_context` / 截图核对结构，未凭空写色值
- [ ] 已建立 Figma 可见资产清单，并逐项确认原始图片/SVG/mask/徽标/icon 是否已复制到项目
- [ ] 关键品牌/图标资产已具备捕获友好版本，且不是仅靠 CSS mask、远程图或浏览器合成效果显示
- [ ] **资产已下载到本地，且已执行格式校验**（`file` 命令确认后缀与内容一致）
- [ ] **所有可见 icon / 插画 / 徽标均已使用真实资产或等价实现，不存在交付型占位**
- [ ] **资产清单文件已创建**（Vite/Webpack 项目：`index.ts` 集中导入导出）
- [ ] HTML 截图与 Figma 截图**同尺寸策略**
- [ ] HTML 截图优先通过 Chrome 插件只读能力或无头 Chrome 完成，且没有不必要地抢夺用户当前 Chrome 焦点
- [ ] 已产出差异说明（或「通过」）
- [ ] 当前轮次 ≤ 5

---

## 与项目文档的配合

若仓库存在 **`DESIGN.md`** 或设计系统文档：

- 复刻时**优先**对齐 Token（主色、中性色、圆角、阴影）。
- 截图差异若来自 Token 与 Figma 单文件不一致，应在结论中**显式说明**并建议产品确认以哪一侧为准。

---

## 版本与维护

- **v1.4** — 截图对比默认使用 Chrome 插件只读截图或独立无头 Chrome，避免非必要抢夺用户当前 Chrome 焦点。
- **v1.3** — 新增「可迁移资产规则」：关键 logo / icon / mask 资产必须生成捕获友好版本，避免 HTML 回流 Figma 时出现空白、纯色块或失真。
- **v1.2** — 明确默认验收口径为 **1:1 视觉复刻**；新增「真实性规则」与「禁止交付型占位」约束；要求未做双端截图对比前不得宣称完成。
- **v1.1** — 新增「资产管理规范」章节：格式校验、Vite 最佳实践、资产清单模式；补充浏览器截图工具要求。
- **v1.0** — 初始版本：三阶段工作流 + 5 轮迭代环。
- 本 skill 描述**流程与验收方式**，不绑定具体 CLI 命令；实施时可将工具写入项目 `package.json` 脚本以便一键跑对比。
- 若团队改用其他对比工具，只需替换「阶段 2」中的工具名，工作流三阶段保持不变。
