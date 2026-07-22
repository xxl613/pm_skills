# &lt;项目名&gt; · 设计语言（DESIGN.md）

> **UI 层真源（人可读）**。本文件定义项目视觉设计语言（从目标 Figma 剥离而来）。
> 分工：**这里写「语言 / 理由 / 规则 / 令牌之外的决策」+ §9 令牌契约**；具体色值/字号等
> 落在 §9 契约与 `theme.css`。**§9 契约 ⟷ `theme.css` 由 `check-design.py` 机器校验一致**
> （漏实现 / 野令牌 / 值漂移即拦）。人话区只引用令牌名，不重复写值，避免三处各写。
> 来源 Figma：`<file key / 链接>`　剥离日期：`<YYYY-MM-DD>`

---

## 1. 主题色（语言 + 理由，值见 §9）
| 角色 | 用法 / 理由 | 令牌 |
|---|---|---|
| 品牌主色 | 仅强调 / 主 CTA，主体克制为灰阶 | `--v5-color-brand` |
| 成功 / 警告 / 错误 | 语义状态，配对浅底 `*-bg` | `--v5-color-success` / `-warning` / `-error` |
| 背景 / 表面 / 描边 | 页面底 / 卡片弹层 / 分隔 | `--v5-color-bg` / `-surface` / `-border` |
| 文本 主/次/三级 | 正文 / 描述 / 文字按钮 | `--v5-color-text` / `-secondary` / `-tertiary` |

## 2. 字体（理由，值见 §9）
- 字体族选型理由 / 中英文回退：　→ `--v5-font-family`

## 3. 字号阶梯（语言，值见 §9）
| 级别 | 字重 / 用途 | 令牌（字号 + 行高） |
|---|---|---|
| 区块标题 | 600 · 区块/卡片标题 | `--v5-font-size-title` / `--v5-line-height-title` |
| 正文 | 400 · 对话/卡片正文 | `--v5-font-size-body` / `--v5-line-height-body` |
| 说明 | 400 · 表格/label/辅助 | `--v5-font-size-caption` / `--v5-line-height-caption` |

## 4. 标题样式 H1–H6（base 无，按需新增；令牌进 §9）
> base 仅 3 档字号。若设计语言需要更细标题阶梯，在此定义语义，并在 §9 / theme.css **新增**
> 对应的 H1–H6 字号令牌（check-design 会要求新增令牌也登记在 §9 契约里）。

| 级别 | 字重 × 行高 × 间距（语言） | 令牌 |
|---|---|---|
| H1 |  |  |
| H2 |  |  |

## 5. 间距 / 圆角 / 阴影（用法，值见 §9）
- 间距 `--v5-space-1..6`（4/8 基数） · 圆角 `--v5-radius-sm/md/lg/pill` · 阴影 `--v5-shadow-card/-overlay`
- 是否沿用 base 还是改：（改了的写进 §9）

## 6. 用法规则 + 反例
- 品牌色何时用 / 何时克制：
- 对比度底线（正文 WCAG AA）：
- 反例（不要做）：

## 7. ⟷ theme.css 映射核对
- [ ] §9 契约每条都已落进 `theme.css`（`check-design.py --check` 通过）
- [ ] `theme.css` 没有未登记进 §9 的「野令牌」

## 8. 令牌之外（CSS 表达不了、必须文字固化）
> 这一节专门接住 tokens/theme.css 表达不了的设计决策，是 DESIGN.md 不可被 CSS 替代的价值。
- **标题阶梯**：H1–H6 超出 base 3 档的部分（语义 + 何时用，值在 §4/§9）。
- **交互状态**：hover / focus / pressed / disabled 的处理（base 缺 hover-dark，如何补）。
- **语义角色**：近黑主按钮 vs 品牌蓝 CTA 各自何时用；次/文字按钮边界。
- **组件组合范式**：本项目新造的卡型 / 状态条 / 交接条等结构（可回收进技能组件库）。
- **动效与插画 / 渐变**：尺度、时长、reduced-motion；插画风格与禁区。
- **用法纪律与反例**：品牌色克制、对比度底线、不堆装饰。

## 9. 令牌契约（机器校验源 ⟷ theme.css）
> 本块是 `check-design.py` 解析的**唯一机器源**：内容应与 `theme.css` 的 `:root` 逐条一致。
> 只写**本项目覆盖 / 新增**的令牌；空 = 完全沿用 V5 base。改视觉＝改这里 + 同步 theme.css。

```css
:root {
  /* 示例（按项目风格填，删掉用不到的）：
  --v5-color-brand: #xxxxxx;
  --v5-font-family: "…";
  --v5-radius-md: 0px;
  --v5-font-size-h1: 32px;   // base 无、新增
  */
}
```
