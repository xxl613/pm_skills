# 数据自洽与逐页 PRD 合成测试样例

这个目录是技能的可运行自测材料，**不是用户已确认的真实业务方案**。所有记录、标题和状态均由本次技能实施创建，只有验证 CRUD、跨页统计与评审工具的用途。`data.json` 明确使用 `fixtureOnly:true`；模拟规则保持 pending，`userReviewed` 始终为 false。

从 `prototype/index.html` 打开。页面列表图标可进入全部记录、统计和“仅未完成”状态场景；旁边文档图标查看各自完整 PRD。建议先通过本地 HTTP 测试跨页持久化：

```bash
python3 -m http.server 8765 --directory prototype
```

浏览 `http://localhost:8765/index.html`。离线阅读数据已嵌入，可通过 file:// 看页面与 PRD；各浏览器对 file:// localStorage 共享行为可能不同，跨页 CRUD 的权威验证使用同一个 HTTP origin。

验证路径：初始 3 条记录（2 未完成、1 已完成）→新增 1 条→统计变为 4/3/1→编辑标题→切换完成状态→统计实时派生→取消删除无变化→确认删除后总数减少。两个页面共享 `store.js` 的同一个 storage key；没有第二份统计样本。重置仅清除此样例自己的 key。

第三场景为 `summary.html?view=active#records`，单独绑定 `prd/active.md`，用来检验同文件 query/hash 的准确 PRD 匹配。未登记 query/hash 显示明确未绑定状态。

标准件的局部复用另见包内 `examples/component-reuse`；本例只验证记录、统计与逐页 PRD 的一致性。

本次已完成的验证与限制见 [验证记录](VERIFICATION.md)。`verified:true` 来自实际 HTTP 浏览器走查；不代表用户已评审，也不表示 file:// 已完成浏览器实测。
