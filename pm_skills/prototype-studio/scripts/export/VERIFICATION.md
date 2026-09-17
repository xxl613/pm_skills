# 导出工具验证记录

2026-09-06，本机 Python 3、Pandoc 与 python-docx 环境。

- `python3 -m unittest discover -s scripts/export/tests -v`：12 项通过。覆盖多文件 JS/CSS/Markdown/ZIP、JS 中页面引用、断链、模块与动态 import、fetch、注释、URL 构造器、远程资源、符号链接、已存在输出、缺失合同，以及真实中文 Word 的标题/表格/图片/列宽/去除首标题和依赖缺失。
- 从本包 coherent-project 示例复制出独立原型目录，生成并注入审阅资源后调用 direct 打包：同步检查和项目检查均退出 0；原始三 JSON、全文 PRD Markdown、完整 `_review` 目录被保留；断链 0；ZIP CRC 检查通过。示例处于并行完善阶段，文件体积不是后续版本的固定基线。
- 27 份迁入动效参考有实际源代码，提取出 98 个片段；其中 17 个 JS 片段通过 `node --check`。本地 UI/UX 查询脚本实际查询成功。

这些记录只证明已列出的静态、结构和本机导出行为。导出脚本不声明浏览器交互、断网可用、Figma 同步或 Word 可见排版已通过。真实渲染和跨页操作的证据由每次交付报告另行记录。JS 扫描不是完整 AST 分析，复杂模板、正则、动态拼接和后端行为必须通过浏览器验证。
