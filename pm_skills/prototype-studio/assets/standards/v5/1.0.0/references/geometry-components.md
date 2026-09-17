# V5 几何、基础组件与皮肤

范围是当前选用的 V5 区域。源代码位置相对包根。以下数值是旧设计规范和当前代码的基线，未在本次重新请求 Figma 验证；精确来源限制见 [验收](verification.md)。

## 令牌与视觉层级

优先复用 `assets/tokens.css` 的现有变量。没有现成变量的元素级尺寸沿用所选组件代码并注明用途；不执行旧版“任何裸值都错误”的机械规则。

| 语义 | 基线 | 用途 |
|---|---|---|
| brand/info | `#1546f2` | 页面主 CTA、选中、链接，主体保持灰阶 |
| success/warning/error | `#00c261` / `#ffa200` / `#ff2626` | 成功/警告/危险，须配文字或图标 |
| success/warning/error/info 浅底 | `#edfaf4` / `#fffaf2` / `#fff1f0` / `#f2f7ff` | 校验与状态，不作无语义装饰 |
| bg/surface/border | `#f7f8fa` / `#ffffff` / `#e5e6eb` | 应用浅底、白表面、1px 分隔 |
| text/secondary/tertiary/disabled | `#1d2129` / `#86909c` / `#4e5969` / `#c9cdd4` | 正文、说明、次操作、占位/禁用 |
| fill | `#f2f3f5` | 次操作填充、控件 hover |
| 字体 | PingFang SC 与系统字体栈 | 本地可用字体，不增加外网依赖 |
| 区块标题/正文/说明 | 24/36 · 16/28 · 14/26 | 细分组件字号以其代码为准 |
| 间距 | 4、8、12、16、24、32 | 对应 `--v5-space-1..6` |
| 圆角 | 4、8、16、999 | badge、按钮、卡片、胶囊 |
| 阴影 | card / overlay 两级 | 普通卡扁平；抬升态/浮层才有影 |

不能为了复制这一标准，把非 V5 宿主的全局 body、按钮和全部主题改成 V5。框架项目用作用域样式/组件边界；独立预览可 iframe 隔离。

## 桌面完整页面与局部使用

| 结构 | 代码/尺寸 | 使用边界 |
|---|---|---|
| 门户 A | `assets/examples/home-portal-full.html`；导航 80、内容列 920；无对话顶栏 | 仅指定 V5 品牌门户时固定 `home-agent-cast.png` 群像，等比完整显示 |
| 对话 B | `assets/examples/chat-flow-full.html`；导航 80、顶栏 60、内容列 840、输入台约 840×136 | 无常驻 300px 会话栏；完整标准对话使用历史轨道 |
| 抽屉 C | `assets/examples/chat-flow-execution.html`、`assets/shell/drawer.html` | 500px 为既有基线；720px 半屏为派生规格，非 Figma 实测 |
| 抽屉结构 | 标题/关闭 → 可滚内容 → 底部操作；白底左边框，不堆阴影 | 主列 `min-width:0`，随抽屉收窄；不要重复侧栏 |

桌面视觉基准是 1440。是否按视口等比显示由宿主交付方案决定，局部标准件不强加全站缩放脚本。真正需要独立列表/详情/管理页时允许建立页面，仍遵守已选组件规范；A/B/C 是可选样式，不是产品信息架构上限。

完整 V5 门户的 Agent 入口直接到相应对话；快捷入口标题同一字号字重，不放大首字/emoji。项目产品身份和导航项目来自用户需求，不从样例复制整套“高校教师”业务。

## 基础组件选用

| 组件与代码 | 固定设计细节 | 接线要求 |
|---|---|---|
| dialog：`assets/components/dialog.html` | 视口居中，遮罩 .45；宽 sm144/md480(派生)/lg832；圆角12；头/正文/底三段；高内容限制视口并滚动正文 | 焦点进入、Tab 不逃逸、关闭后回触发器；取消无副作用；危险确认说明对象和影响 |
| form card：`assets/components/card.html` | `.v5-card`，浅底描边圆角16、padding24；白内容块；标题18/26、正文16/28；普通无投影 | 用于表单/弹窗内容；不要替代对话 `.v5-rcard` |
| button：`assets/components/button.html` | lg40/md36/sm28；卡内/弹窗主操作近黑；页面 CTA 品牌蓝；次按钮白描边或浅填充 | 有 hover/focus/disabled；按钮标明结果动作；危险使用 error 色 |
| form：`assets/components/form.html` | 单行高38，白底1px描边，胶囊，横padding12，14/22；label上方、间距8 | focus/error/disabled；错误给修正路径；真实 input/select 与可访问标签 |
| table：`assets/components/table.html` | 浅灰表头、白行、1px分隔、圆角16；横padding16 | 数据共享，排序/分页/空态要有逻辑；不能只有可点击外观 |
| pagination：`assets/components/pagination.html` | 页码约32；当前近黑白字；前后页可禁用 | 总数与列表同源；筛选后当前页合法；保留空态 |
| toast：`assets/components/toast.html` | 顶中轻提示、白底、浮层影；四语义图标/文字 | 只承载短反馈；需要决定时用确认层；不伪报保存/提交成功 |
| empty-state：`assets/components/empty-state.html` | 图标64–96、说明、可选近黑操作 | 说明为何为空及第一步；区分首次为空、搜索无结果、加载失败 |

对话输入台和文件卡见 [对话交互](conversation.md)，对话结果卡见 [结果卡](result-cards.md)，手机专用布局见 [移动端](mobile.md)。

## 品牌皮肤的受限覆盖

用户指定“保留 V5 交互结构，套项目皮肤”时，抽取项目 Figma 的颜色/字/间距/圆角/效果及其用法，写到项目设计简报；再派生作用域内的 theme CSS。文档与 CSS 同一更改同步。保留近黑确认与页面 CTA 的角色、hover/focus/disabled、动效与组件层级，不只搬颜色。

Figma 的品牌/语义色映射到 `--v5-color-*`；字体与标题阶梯映射 `--v5-font-*`/`--v5-line-height-*`；空间/圆角/阴影映射对应现有变量。仅写差异和确实需要的新令牌。缺失变量不得臆造为 Figma 原值；记录推导。

如果用户指定的是整体布局/结构也变化，应重新定义组件变体或新标准，不冒称“仅换皮”。Figma 实际读取走当前已安装官方技能/工具；不继续旧文档“固定 Dev Mode/重启旧客户端/固定 MCP 接口”的过时要求。
