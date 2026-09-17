# 标准包契约与工具

每包位于 `assets/standards/<id>/<version>/`，含 `pack.json`、包内 references 规范与完整运行依赖；根 references/standards 是索引。文件级哈希只证明复制保全；实际页面是否采用、交互是否正确、视觉是否一致分别验证。

## 登记输入

`register_standard.py --source <已自包含目录> --definition <定义JSON> --registry <标准库目录>`。

定义 JSON 必填：id、version（major.minor.patch）、title、platforms（非空列表）、scope（适用页面/区域）、locked（不可改项列表）、slots（可变内容列表，可为 []）、states（状态列表）、examples（包内 HTML 路径列表或含 path 的对象）、source（真实出处）、license（已知许可或 unknown）。

有详细规范时定义 specification.entry（包内规范入口）、specification.files（规范文件列表）；规范文件与代码同样锁定哈希，更新版本时一起更新。

工具逐文件保存原始路径、原始 SHA256、复制后 SHA256、改动说明。同版本拒绝覆盖；符号链接和逃逸目录不接受；运行资源必须在包内，外部普通超链接单独报告。不要在包里放凭据、缓存、node_modules 或无关历史文件。

例子中 [definition.json](../../examples/component-reuse/definition.json) 与 [source](../../examples/component-reuse/source/index.html) 可直接运行；不要把样例业务值当项目真实数据。

## 复用接口

`install_standard.py --pack <版本目录> --target <项目根>` 只复制固定版本到 `standards/<id>/<version>/`，生成 `standard-usage.json`。

默认业务原型只使用上述资源安装方式，再把选定 HTML/CSS/JS 接入当前文档的原生 DOM。不得为隔离样式用 iframe 套壳业务页面，否则浏览器采集插件可能无法选择内部元素。

仅当用户明确要求独立的标准件演示/隔离测试样例时，可在样例页面放一个 `<!-- STANDARD-MOUNT:区域ID -->`，再加参数：`--page <项目内HTML> --scope <区域ID> --entry <包内HTML> --height 360`。工具只替换该精确标记为 iframe，保留 CSS/JS 隔离，并在使用锁记录页面、区域、入口及包哈希。此模式不是业务页交付方式，不得自动采用。不会自动推断 DOM，也不覆盖已漂移版本。

需要共用宿主数据和事件的真实组件由实施者复制选定 HTML/CSS/JS 并手工接入；必须记录具体消费范围与允许的业务差异，并运行浏览器验收。assets-only 记录不证明页面已消费；现有检查器也不自动证明手工 DOM 集成。

## 检查与版本

- `check_standard.py --pack <版本目录>`：文件完整性、哈希、声明样例、静态 HTML/CSS/模块引用。
- `check_standard.py --project <项目根>`：使用锁、已安装版本完整性、明确 iframe 区域是否仍引用锁定入口。
- JS 动态路径、条件加载、iframe 内实际交互、像素差异需要浏览器验证。检查报告明确这一边界。
- 更新先登记新版本并列出影响；旧版本只读。结构/事件不兼容升 major；兼容能力增加升 minor；兼容修复升 patch。项目切换新版是显式任务。

`migrate_v5.py --source <旧技能备份目录> --specifications <本版包内references目录> --registry <新标准库>` 仅用于复建一次性迁移，必须显式提供保留的源备份和已整理的规范目录，不从旧规范自动推导新规则。日常使用、验证、打包均不依赖旧技能目录；pack 中绝对源路径仅作出处记录，不会被运行时代码读取。
