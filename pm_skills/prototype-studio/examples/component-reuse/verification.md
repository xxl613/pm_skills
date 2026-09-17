# 标准件登记与复用验证

本目录演示用户提供的自包含组件目录，经登记形成版本包，再复用到两个页面。固定说明文本不是产品业务数据。

- 源目录：source/，包含 HTML、CSS、JS 三个文件。
- 定义：definition.json，声明适用范围、锁定内容和展开/收起状态。
- 登记结果：registry/resource-note/1.0.0/pack.json。
- 消费结果：project/index.html、project/second.html，共用 project/standards 下同一版本。
- 使用锁：project/standard-usage.json，明确两处页面、区域、入口与 manifest SHA256。

## 已执行

`python3 scripts/components/test_components.py` 的 9 个测试通过：第一次登记与第二页复用、同版本拒绝覆盖、缺失资源拒绝登记、代码哈希漂移检出、消费挂载漂移检出、无明确挂载标记时页面不变、符号链接拒绝登记、规范缺失拒绝登记、版本规范随包复用。

实际 Chrome 152.0.7977.76 浏览器验证见 [browser-report.json](evidence/browser-report.json)：两个页面分别通过 HTTP 和 file:// 运行，展开/收起和 aria-expanded 同步，宿主标题样式未受 iframe 内 CSS 污染。

V5 标准包登记 184 个文件（177 个源资产/独立入口与 7 个版本化规范/覆盖文件；不包含 Finder 元数据），本地引用与哈希检查通过。浏览器覆盖 4 个桌面完整样例、11 个移动完整样例的实际渲染和图片加载，无页面 JS 异常或资源请求失败。桌面历史轨道实际验证 query 当前项/刻度、非法 query 回退、hover 展开、Escape 收起与保留焦点、模态隐藏及 16 个链接退出/恢复键盘顺序。截图存于 evidence/。

## 验证边界

标准包完整不等于业务页面已采用标准；assets-only 使用锁也不等于已挂载。iframe 验证只适用于明确独立嵌入的区域，手工接入宿主 DOM 的组件需另做验证。

旧完整样例中其余按钮仍有静态示范内容，本次未把它们宣称为完整交互产品。未重新连接 Figma 或进行新导出像素对比。原有 figma-reference 是旧组件渲染基准，移动部分来源有版本差异；图片加载成功不证明旧样例业务文案的数据一致性。

运行浏览器测试需要当前环境已存在 Playwright 与 Chrome：`node scripts/components/test_components_browser.cjs`；按实际环境设置 NODE_PATH，不自动安装依赖。
