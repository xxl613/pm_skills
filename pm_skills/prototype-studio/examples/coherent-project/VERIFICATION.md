# 合成样例验证记录

2026-09-06，使用 macOS Chrome、CUA 浏览器工具，通过 `http://127.0.0.1:8765` 实际操作。所有数据为可恢复的独立技能测试记录；测试后恢复初始三条记录。

| 检查 | 实际结果 |
|---|---|
| 新增 | 从 3/2/1 变为 4/3/1 |
| 编辑与完成 | 统计页读到更新后的同一标题，数量为 4/2/2 |
| 取消删除 | 数量仍为 4/2/2，记录保留 |
| 确认删除 | 统计页为 3/2/1，新增记录消失 |
| 删除至空态 | 统计页为 0/0/0，出现明确空态 |
| 恢复 | 重置后恢复 3/2/1，仅操作样例 storage key |
| 三份 PRD | 全部记录、统计、query/hash 过滤状态分别显示正确文档 |
| 未登记状态 | query 改为未登记值时明确报无绑定，不回退到错误 PRD |
| 页面列表 | 三入口都存在，路径含完整 query/hash，状态分列 |
| 键盘 | Escape 关闭并返回图标焦点，Tab/Shift+Tab 在面板循环 |
| 视觉 | 已目视检查桌面 PRD 浮层、滚动阅读区域、来源提示和三项状态 |

自动验证命令均从技能包根目录执行：

```bash
python3 -m unittest discover -s scripts/sync -p 'test_*.py' -v
node examples/coherent-project/test-store.cjs
node --check assets/review-shell/review-shell.js
node --check examples/coherent-project/prototype/app.js
python3 scripts/sync/sync_review.py --project examples/coherent-project/prototype --check --inject
python3 scripts/check/check_project.py --project examples/coherent-project/prototype
```

同步回归的 9 项测试覆盖全篇离线内容、query/hash、重复路由规范化、缺失/空 PRD、越界路径、用户评审证据、默认不注入、只读陈旧检查、注入幂等、损坏受管块不写半成品、性能确认表证据保留。共享 store 测试使用两个独立 JavaScript 上下文和同一持久层验证跨页 CRUD 与派生数量。

另有根任务独立测试的 [导出副本浏览器记录](evidence/browser-report.json)：Chromium 149 对工作目录中的导出副本启用断网模式，验证完整 PRD、跨文件 CRUD、query/hash、390px 评审浮层边界，未报告 JavaScript 错误。对应截图为 [场景 PRD](evidence/offline-scene-prd.png)、[页面列表](evidence/offline-page-list.png)、[移动宽度 PRD](evidence/offline-mobile-prd.png)。这份独立测试在得知下述拒绝之前启动，不是对被拒源路径的重试。

限制：CUA 浏览器工具明确阻止访问源目录的 file:// 路径，未绕过；源目录的本代理走查仅通过 HTTP。独立导出副本的离线结果只适用于该 Chromium 和样例，不推断所有浏览器的 file-origin 行为。尚未做真实移动设备或屏幕阅读器专项验证；未调用真实 AI，也没有真实性能测量。`fixtureOnly` 检查通过只说明技能自测一致，不能代表真实产品数据已确认。
