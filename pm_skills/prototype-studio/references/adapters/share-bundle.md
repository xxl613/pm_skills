# 分享包验证与限制

`package_prototype.py`对明确指定的原型根创建新目录，不覆盖旧包。排除隐藏文件、node_modules、版本控制、缓存、测试和脚本开发目录；保留md/json和运行JS/CSS/图片/字体。源内symbolic link拒绝，避免交付依赖外部路径。

直接打开模式保存普通script/style/link的顺序与相对地址，不做脆弱的“只内联第一个JS/CSS”。外部module、import、动态import、import.meta、fetch/XHR、Worker/ServiceWorker/WebSocket/源站路由依赖需要本地server或专门适配；脚本明确拒绝风险，不谎称Vite代码分割已经离线。

静态扫描识别HTML属性、CSS url/import与JS字符串中的常见资源；先跳过JS注释，减少注释触发。构造式路径、运行时用户输入和后端行为仍不能穷尽。server模式把风险列入manifest，不静默修业务代码。

验证顺序：源审阅同步check→复制与引用检查→ZIP完整性→从解压产物实际浏览。测试入口、页面目录、每页全文PRD、多页面JS/CSS、图片、导航和关键交互。断网测试通过才称离线。反馈文件大小构成、重复资源、未优化项和确实完成的验证。
