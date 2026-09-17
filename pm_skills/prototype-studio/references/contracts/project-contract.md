# 原型项目合同 v1

本合同由产品规格能力维护；实现消费合同，评审壳呈现合同，验收检查合同，交付保留合同。`_review/` 是可再生成阅读视图，不可手改为第二个来源。源文件中的用户决定必须来自实际用户答复。

本合同的完整文件和路径检查用于已接入的可运行原型。纯规划阶段先维护页面计划和 PRD，允许已确认内容尚未实现；制作原型时再使登记路径指向真实页面，不用空页面或占位 JSON 冒充已完成接入。

## 目录和页面

```text
prototype/
  pages.json
  data.json
  decisions.json
  prd/*.md
  页面及共享运行资源
  _review/                   # sync_review.py 生成
```

三个 JSON 均为 UTF-8、`schemaVersion: 1`。路径相对于项目根；禁止绝对路径、网络路径或越出项目。`pages.json` 的结构为：

```json
{
  "schemaVersion": 1,
  "projectId": "stable-project-id",
  "title": "项目名称",
  "pages": [{
    "id": "records", "title": "记录列表", "path": "index.html",
    "prd": "prd/records.md", "dataObjects": ["record"],
    "status": {"implemented": false, "verified": false, "userReviewed": false}
  }]
}
```

- `id` 唯一且稳定；`path` 为真实 HTML，可包含 query/hash；同一文件不同状态场景分别登记，不能为可截图状态发明新业务页面。
- 当前页按解码 pathname、排序后的完整 query 键值对、解码 hash 匹配，不丢弃 query/hash。登记路径唯一；未知路径显示“未绑定”，不借用别的 PRD。
- `prd` 必须指向非空 Markdown，全文离线嵌入。每个登记入口绑定一份对应 PRD；多个同业务场景可以通过相互链接说明关系。
- `dataObjects` 引用 data.json 中存在的对象 ID。
- `status` 三个布尔值独立。`userReviewed: true` 必须有同级 `userReviewEvidence` 字符串说明实际用户确认；工具不设置该状态。已评审内容发生实质变化后将其改回 false，保留历史证据到项目变更记录。
- 空 `pages: []` 只用于尚未制作的项目：评审面板有明确空态，正式完成不得把空目录算成原型。
- 验收枚举业务 HTML 并检查本地业务链接。`assets/`、`standards/`、`_review/` 等运行支持目录不按业务页扫描；其他非业务 HTML 必须在 `supportingHtml:[{path,reason}]` 中说明用途，不能用它隐藏真实功能页。动态生成入口仍需浏览器走查。

## 对象、字段与 CRUD

`data.json = {schemaVersion:1, objects:[...]}`。仅技能自测可附 `fixtureOnly:true`，所有产物必须显著标明合成测试，不能将其改作真实业务授权。

```json
{
  "id": "record", "title": "记录",
  "fields": [{
    "id": "title", "type": "string",
    "source": {"kind": "user-input", "reference": "index.html 的记录表单", "pages": ["records"], "rule": "用户输入并保存"}
  }],
  "crud": {
    "create": {"mode": "interactive", "pages": ["records"], "rule": "保存后创建记录"},
    "read": {"mode": "interactive", "pages": ["records"], "rule": "展示共享记录"},
    "update": {"mode": "interactive", "pages": ["records"], "rule": "编辑同一 ID"},
    "delete": {"mode": "interactive", "pages": ["records"], "rule": "确认后移除，取消无变化"}
  }
}
```

字段可附 `pages:[pageId]` 精确记录消费页；省略时按对象的全部消费页核对。它与 `source.pages` 的输入/来源页用途不同。

字段 `id` 在对象内唯一；`type` 为 string/number/boolean/date/enum，可附 `example`，它是例值而非来源证据。source 含 kind、非空 reference、pages；没有来源页时 `pages:[]` 并补 `noPageReason`，例如外部导入任务或后台配置，不虚构前台页面。

| source.kind | 必须解释的来源规则 |
|---|---|
| user-input | 指明输入页面和保存动作；新建后跨页共享 |
| external | 必填同步 `rule` 和 `maintainer`；项目内来源文件用 `artifact`（存在的相对文件路径），否则用 `externalSystem` 标识实际系统；无来源页要写原因。外部系统真实性仍需人工核验 |
| derived | 必填 `inputs:["对象ID.字段ID"]` 和 `rule`，引用存在；展示值从输入计算 |
| fixed | 必填 `storage`：database-seed / maintained-config / prototype-example，以及说明为何固定的 `rule`、维护者 `maintainer`；无默认选择 |
| ai | 必填输入字段 `inputs`、更新触发和缓存/重算 `rule`、`performanceDecisionId`；关联 performance 的 affectedPages 必须覆盖字段消费页 |
| synthetic | 必填 `decisionId` 指向用户确认的 mock-rule；`rule` 描述模拟范围和一致性。fixtureOnly 自测例可指向 pending mock-rule，但不能伪称确认，rejected 在任何模式都不可使用 |
| pending | 必填 `decisionId` 指向 pending data-source。可暂缺 reference；不得作为正式已定义字段交付 |

对象 `crud` 必须逐项交代 create/read/update/delete。mode 为 interactive/external/derived/fixed/not-applicable；每项 rule 非空，pages 引用真实页面；interactive 至少一个页面。其余模式 pages 可以为空，rule 交代维护者和原因。计算对象通常 read 可见、增改删为 derived；不可对计算结果增设误导性编辑按钮。

业务 fixture 的数据真源可以是 JSON 或共享 JS；所有消费页复用它，不能复制不同数值。数据合同描述语义与来源，原型状态存储是另一层，不能把 localStorage 当作计划中的真实后端。

## 决策与性能确认

`decisions.json = {schemaVersion:1, decisions:[...]}`。每项 id 唯一，kind 为 data-source/performance/scope/mock-rule，status 为 pending/confirmed/rejected，包含 question 与 affectedPages。confirmed 必须有非空 answer 和 evidence（实际用户答复/记录），不能由创建原型或脚本成功推断。

performance 记录增加：

```json
{
  "id": "PERF-001", "kind": "performance", "status": "pending",
  "question": "是否需要每次操作后重新生成 AI 摘要？",
  "affectedPages": ["records"],
  "performance": {
    "trigger": "记录变化", "frequency": "每次保存",
    "impact": "增加等待与模型调用；未实测", "alternative": "按需生成并缓存",
    "measurement": "unknown", "highCost": true,
    "assessmentBasis": "每次保存新增模型请求，存在等待和调用费用，尚未实测"
  }
}
```

`assessmentBasis` 说明成本判断依据，不能仅填 highCost false 就视为无影响。低成本项仍为 pending 时在报告保留提示；高成本 pending 阻止正式完成。证据字段只能检查存在，真实用户确认由执行者核对。measurement 为 estimated/measured/unknown；没有实测不得填虚构延迟或费用。measured 必须附非空 `performance.evidence`，写明测量环境、方法与结果；estimated 建议注明估算假设，未知就写 unknown，不把估算当测量。highCost true 且 pending 可用于探索，正式交付必须阻止。脚本从同一记录生成 `_review/performance-review.md`，页面 PRD 面板展示当前页面确认表（字段、触发、频率、影响、替代、测量类型与证据、决定、用户证据）。

## 同步和新鲜度

```bash
python3 scripts/sync/sync_review.py --project /absolute/prototype
python3 scripts/sync/sync_review.py --project /absolute/prototype --inject
python3 scripts/sync/sync_review.py --project /absolute/prototype --check --inject
```

生成 `_review/review-data.js`、`review-shell.js`、`review-shell.css`、`performance-review.md`、`source-manifest.json`。read-only `--check` 返回 1 代表缺失、陈旧或非法输入；正常返回 0，命令行参数错误返回 2。`--inject` 仅对 pages.json 登记的 HTML 加/修受管引用块，不改业务主体；只运行默认同步不会接管业务代码。普通 `--check` 检查派生内容和已有受管块，带 `--check --inject` 才会要求所有登记 HTML 均已接入；总验收必须使用后者，避免只有文件却无入口。框架应在公共 HTML 入口接入相同受管块；无法这样集成的真实框架必须单独提供浏览器的导航与逐页 PRD 证据，不能把普通 `--check` 当作接入已通过。

源摘要覆盖三个 JSON 与所有绑定 PRD，生成物字节同时检查；不覆盖任意业务代码，不能声称它证明“代码语义自动同步 PRD”。每次业务设计改变后，先让技能更新 PRD/合同，再运行生成器。运行时不 fetch、不依赖网络，支持解压后 file:// 打开；完整 Markdown 原文始终可查看，常用标题/段落/列表/表格/代码渲染为阅读版。

框架路由接入还需核对已打开面板的更新：当前运行时监听 `popstate` 和 `hashchange`，每次打开面板时也会重新匹配路由；单独调用 `history.pushState` 或 `replaceState` 不会刷新已打开的 PRD。项目采用这类路由时，应在框架路由完成回调中接好面板更新并实际验证，不能仅凭静态注入就宣称已支持场景切换。

验收还需检查来源、计算依赖、用户确认、跨页 CRUD 与标准件，单独同步检查不能替代这些内容。
