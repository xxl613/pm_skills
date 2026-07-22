# 01 · 设计令牌（tokens.css 取值表 + 用法）

> 全部为 Figma「全自动课程助教 V5」实测值（少数标「派生」）。文件：`assets/tokens.css`。
> **铁律：定制页面所有颜色/字号/间距/圆角/尺寸必须用 `var(--v5-*)`，禁止写裸值。** 这是「跨项目零漂移」的根本。

## 颜色

| 令牌 | 值 | 用途（何时用） |
|---|---|---|
| `--v5-color-brand` | `#1546f2` | 品牌蓝。**仅强调**：页面级主 CTA、选中态、链接。UI 主体克制为灰阶 |
| `--v5-color-info` | `#1546f2` | 信息语义（同品牌蓝），浅底 `--v5-color-info-bg` |
| `--v5-color-success` | `#00c261` | 成功语义，浅底 `--v5-color-success-bg` |
| `--v5-color-warning` | `#ffa200` | 警告语义，浅底 `--v5-color-warning-bg` |
| `--v5-color-error` | `#ff2626` | 错误/危险语义，浅底 `--v5-color-error-bg` |
| `--v5-color-success-bg` / `-warning-bg` / `-error-bg` / `-info-bg` | `#edfaf4` / `#fffaf2` / `#fff1f0` / `#f2f7ff` | 语义浅底：状态卡/Toast/危险按钮 hover |
| `--v5-color-bg` | `#f7f8fa` | 应用背景 / 浅灰底（卡片默认底、表头、hover 底） |
| `--v5-color-surface` | `#ffffff` | 白色表面：卡内内容块、弹层、输入框 |
| `--v5-color-border` | `#e5e6eb` | 描边 / 分隔线 / 表格边框（1px） |
| `--v5-color-text` | `#1d2129` | 正文主文本；**也是近黑主按钮底色** |
| `--v5-color-text-secondary` | `#86909c` | 辅助/描述文字、次要图标 |
| `--v5-color-text-tertiary` | `#4e5969` | 三级灰：次/文字按钮字色、下拉默认值 |
| `--v5-color-text-disabled` | `#c9cdd4` | 占位符 / 禁用文字 |
| `--v5-color-fill` | `#f2f3f5` | 浅填充：次按钮填充变体底、控件 hover |

## 字体与字号

| 令牌 | 值 | 用途 |
|---|---|---|
| `--v5-font-family` | `"PingFang SC", -apple-system, …` | 全局字体族 |
| `--v5-font-size-title` / `--v5-line-height-title` | 24 / 36 | 区块标题（Semibold） |
| `--v5-font-size-body` / `--v5-line-height-body` | 16 / 28 | 对话正文、气泡、卡片正文 |
| `--v5-font-size-caption` / `--v5-line-height-caption` | 14 / 26 | 表格/说明/label/辅助 |

> 另有更细档（H1 30/42、卡片标题 18/26、说明 12/20）在组件里以字面值+注释处理，未升为令牌（避免档位过密）。

## 间距（4 / 8 基数）

| 令牌 | 值 | 典型用途 |
|---|---|---|
| `--v5-space-1` | 4 | 最小间隙 |
| `--v5-space-2` | 8 | 基础元素间距 |
| `--v5-space-3` | 12 | 控件内距 |
| `--v5-space-4` | 16 | 气泡/区块内距 |
| `--v5-space-5` | 24 | 卡片内边距 |
| `--v5-space-6` | 32 | 大间距/分区 |

## 圆角

| 令牌 | 值 | 用途 |
|---|---|---|
| `--v5-radius-sm` | 4 | 状态 badge |
| `--v5-radius-md` | 8 | 导航激活、按钮、通知 badge、弹层 chip |
| `--v5-radius-lg` | 16 | 卡片 / 气泡 / 弹窗 / 输入台 |
| `--v5-radius-pill` | 999 | 全胶囊：单行控件、品牌 CTA、筛选条 |

## 阴影

| 令牌 | 值 | 用途 |
|---|---|---|
| `--v5-shadow-card` | `0 2 8 rgba(0,0,0,.04)` | 卡片**抬升态**才用（V5 卡片默认扁平，靠描边+浅底，无投影） |
| `--v5-shadow-overlay` | `0 6 40 rgba(0,0,0,.08)` | 浮层：弹窗、下拉、Toast、悬浮菜单 |

## 布局尺寸

| 令牌 | 值 | 用途 |
|---|---|---|
| `--v5-nav-width` | 80 | 左侧导航栏宽（三壳层一致） |
| `--v5-topbar-height` | 60 | 对话流顶栏高 |
| `--v5-content-max` | 840 | 对话流内容列宽（原型 B） |
| `--v5-portal-col` | 920 | 门户内容列宽（原型 A） |
| `--v5-drawer-width-third` | 500 | 1/3 屏抽屉（原型 C） |
| `--v5-drawer-width-half` | 720 | 半屏抽屉（原型 C，派生） |

## 移动端布局尺寸（`--v5m-*`，H5 375×812）

结构实测自 Figma「大平台设计-UI」教师端 app（`ljg4eVP3elzzx5b2Q8FYdI`）。颜色/间距/圆角与桌面共用 `--v5-*`。

| 令牌 | 值 | 用途 |
|---|---|---|
| `--v5m-viewport` | 375 | 移动壳层画板宽 |
| `--v5m-screen-min` | 812 | 移动壳层画板最小高 |
| `--v5m-statusbar-height` | 44 | 模拟系统状态栏（原型演示态） |
| `--v5m-topbar-height` | 44 | 移动顶栏 |
| `--v5m-tabbar-height` | 49 | 底部 TabBar（仅 A-m 一级页） |
| `--v5m-safe-bottom` | 34 | Home Indicator 安全区 |
| `--v5m-page-pad` | 16 | 页面左右内距 |
| `--v5m-font-size-title` / `--v5m-line-height-title` | 17 / 24 | 移动顶栏/页标题 Semibold |
| `--v5m-line-height-body` | 24 | 移动正文行高（16px 字号收紧） |

## 用法约束

1. **禁裸值**：颜色/字号/间距/圆角/布局尺寸一律 `var(--v5-*)`。仅「元素级像素」（图标 20、头像 28/32/36、图标按钮 34 等令牌无对应档的细节）可字面值，且**就近注释**。
2. **品牌色克制**：大面积保持灰阶（bg/surface/border/text 系），蓝色只用于强调与主 CTA。
3. **扁平优先**：卡片/状态块用描边+浅底分隔，不堆装饰阴影；阴影只给真正的浮层。
4. **语义色**：成功/警告/错误/信息只用于状态表达，不做装饰；不靠颜色单独表达状态（配图标/文字）。
