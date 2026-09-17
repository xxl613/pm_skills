---
name: prototype-delivery
description: 校验并交付原型分享包、页面 PRD Word 或 Figma设计稿；保留页面目录、离线PRD、数据来源与标准素材，并区分直接打开与本地服务器模式。
---

# 原型交付

基于已经实现的原型制作可复查的交付件。先确认项目校验、页面登记与PRD同步通过，不能把打包成功当作功能或视觉验收通过。

## 分享文件夹与ZIP

显式选择项目的原型运行目录，不能把整个知识库或工作区打包。根内有 `pages.json` 时，打包器先运行本包的 `sync_review.py --check` 和 `check_project.py`，任一校验器缺失或资料陈旧/不完整则拒绝导出。原始三份JSON、页面PRD Markdown、`_review`及运行资源均保留。

```bash
python3 scripts/export/package_prototype.py --source PROJECT --output NEW_FOLDER --entry index.html --mode direct --zip NEW_ARCHIVE.zip
```

`direct`保留全部页面、普通JS/CSS顺序、图片、字体、PRD和JS中的页面清单，支持多文件静态HTML。它不重写业务代码。发现 ES modules/import、fetch/XHR、Worker、网络接口或其他需要源站的机制时拒绝，不把不完整的Vite内联转换宣称为离线包。

Vite等编译项目先按现有工程构建，用相对资源路径；准备好运行目录及源审阅材料后使用：

```bash
python3 scripts/export/package_prototype.py --source STAGED_DIST --output NEW_FOLDER --entry index.html --mode server --zip NEW_ARCHIVE.zip
```

`server`附 `serve.py`，接收者运行 `python3 serve.py` 后访问提示的本机地址。模块路径仍保持原相对关系，支持多chunk。它不提供后端或代理外部API；网络依赖、需后端的业务和无法静态证明的动态资源必须逐项说明。浏览器断网走查通过后才可称“离线可用”。

新目录/ZIP不覆盖已有文件。脚本校验HTML/CSS/可识别JS引用、资源完整性、ZIP可读性，输出体积、重复文件及风险清单。静态扫描不能证明所有动态运行路径，需开解压产物验证入口、目录、全文PRD、跨页跳转和关键交互。见[打包验证与限制](../../references/adapters/share-bundle.md)。

## PRD 导出 Word

```bash
python3 scripts/export/export_prd_docx.py SOURCE.md OUTPUT.docx --palette blue
```

需要 Pandoc 与 python-docx；可用 `--pandoc EXECUTABLE`、`--reference-doc TEMPLATE.docx`、`--resource-path DIR`、`--font FONT`、`--latin-font FONT` 指定依赖/模板。通过所选 Python 环境安装或提供 `python-docx`，脚本不隐式联网安装。

保留原文、标题、表格、列表、图片与链接；不自动增添封面、目录或介绍。只有明确要求去掉首个H1时使用 `--drop-first-title`。默认蓝色标题、可见表格六边网格、首行底色、A4及中文字体；表格按内容分配宽度。导出后的JSON报告区分XML结构验证与视觉渲染。需要视觉交付时，按可用文档技能渲染并查看页面，未渲染不得称排版验证通过。详见[Word导出](../../references/adapters/prd-word.md)。

## Figma

需要同步到Figma才读[Figma交付适配](../../references/adapters/figma-delivery.md)，按当前官方Figma技能调用工具。业务画布与PRD/目录/调试外壳隔离，真实素材随项目保留。校验状态覆盖、溢出、图层和真实截图，未写入或未读取结果不得宣称同步成功。
