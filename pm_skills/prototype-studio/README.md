# 原型工作室

一个统一入口、五个专项 Skill，以及共用的规格、V5 标准件、视觉方法与交付工具。

日常使用 `prototype-studio`，说明本次要新建、修改、复刻、提取标准件、验收还是导出。技能按范围加载专项，不要求每次走完整流程。

| Skill | 职责 |
|---|---|
| prototype-studio | 任务范围、专项选择、变更同步与完成条件 |
| prototype-spec | 材料、页面 PRD、数据来源、对象生命周期和用户决定 |
| prototype-build | 自主设计、参考复刻、视觉探索与真实交互 |
| prototype-components | 提取、登记、版本化、安装和核对标准件 |
| prototype-qa | 页面覆盖、来源、交互、视觉、标准件与验证证据 |
| prototype-delivery | 离线原型、Word、Figma 及任务要求的发布 |

## 常用请求

- “使用 prototype-studio 制作原型；这一块用 V5 对话流，其余沿用当前设计。”
- “修改这个页面的筛选和统计，检查受影响页面，同步页面 PRD。”
- “把这个区域整理为标准件，保留完整状态、交互和图片。”
- “只做视觉方向探索，业务字段和数据保持一致。”
- “验收后导出离线包，保证页面 PRD 仍可阅读。”

## 项目接入

项目内维护 `pages.json`、`data.json`、`decisions.json` 和各页 Markdown PRD。具体结构见 [项目合同](references/contracts/project-contract.md)；测试项目见 [一致性示例](examples/coherent-project/README.md)。已有项目沿用实际工程，仅适配这份合同，不另建第二套业务数据。

以下命令从本插件根目录执行；将项目参数替换为实际绝对路径：

```sh
python3 scripts/sync/sync_review.py --project /absolute/prototype --inject
python3 scripts/check/check_project.py --project /absolute/prototype
```

首次接入原生 HTML 用 `--inject` 添加页面列表和 PRD 图标。已有框架通过它的 HTML/脚本入口接入相同阅读运行时。检查生成内容时可用 `sync_review.py --check --inject`；业务变化必须先同轮更新原始规格，生成器不会从任意代码中猜测新需求。

每个独立页面与 query/hash 场景都绑定 PRD。阅读内容离线嵌入，全文可见。所有统计来自共享记录。模拟规则需已确认；新增无来源字段和高成本 AI 数据会保留待确认。技能自测明确标记 `fixtureOnly`，不能作为真实项目的确认豁免。

## 标准件与交付

[V5 标准包](references/standards/v5.md) 保留真实资源、交互和页面样例；选定的范围按版本锁定，其他页面沿用项目设计。[标准件合同](references/standards/package-contract.md) 说明提取、登记和复用方式。

[交付专项](skills/prototype-delivery/SKILL.md) 提供离线和 Word 工具及 Figma 适配。需要网络运行时的项目不得被标为可直接双击打开；Figma、发布和实际 AI 调用只在用户任务需要时执行。

## 迁移与验证

[迁移清单](references/migration/skill-map.md) 记录全部 30 个旧技能的去向。官方 Figma、Product Design、Sites 及图像工具仍是按需外部能力，官方 API 只依当前工具契约，不在本包维护副本。

`tests/` 保存可复跑的关键不变量测试。脚本检查、浏览器交互、视觉判断和用户评审分别记录。源文件及本包通过检查，不代替导出后的独立验证。
