# 旧技能能力迁移表

本次按能力拆分，不保留重复的旧综合工作流。旧目录先完整备份，启用新插件后才退出活跃技能列表。官方插件缓存不改；现有业务项目不批量重写。

| 旧技能 | 新维护位置 | 迁移处置 |
|---|---|---|
| v5-prd-skeleton | prototype-spec：材料、来源与候选结论 | 合并并归档旧入口 |
| v5-page-planning | prototype-spec：页面登记、覆盖与 PRD | 合并并归档旧入口 |
| prototype-to-prd | prototype-spec：变更同步 | 合并；代码仅用于发现差异 |
| v5-ux-rule | V5 标准包＋通用 review-shell＋标准检查 | 旧规则归档；保留薄兼容转交入口 |
| figma-prototype-system | prototype-components / prototype-build / review-shell | 拆分并归档旧入口 |
| huashu-design | prototype-build；包外 huashu-presentations | 原型方法合并，HTML 演示能力单独保留 |
| frontend-design | prototype-build | 合并设计实现方法 |
| impeccable | visual-craft | 合并产品/品牌分界与设计方法 |
| redesign-existing-projects | prototype-build：局部修改与精修 | 合并；保留现有功能、内容和栈 |
| ui-ux-pro-max | visual-craft/catalogs＋scripts/design | 保留可查询资料；移除项目专属流程 |
| design-taste-frontend | visual-craft＋styles | 作为场景方法参考 |
| gpt-taste | styles＋motion | 删除模拟执行与任意随机化，只保留有效构图/动效原则 |
| high-end-visual-design | styles/material-depth | 可选风格参考 |
| industrial-brutalist-ui | styles/industrial | 可选风格；无随机业务装饰数据 |
| minimalist-ui | styles/editorial-minimal | 可选风格；不作为全局禁令 |
| image-to-code | prototype-build：复刻与探索 | 视觉来源和业务来源分开 |
| imagegen-frontend-web | prototype-build：视觉探索 | 按需生成，不设图片数量配额 |
| imagegen-frontend-mobile | prototype-build：视觉探索 | 移动布局参考与探索 |
| brandkit | 包外原技能；原型品牌方法进入 visual-craft | 完整品牌设计能力保留 |
| stitch-design-taste | adapters/stitch | 转为按需适配说明 |
| transitions-dev | assets/motion | 保留真实代码、状态钩子与兼容说明 |
| figma-to-html-replica | prototype-build＋adapters/source-replica | 复刻与工具前置规则分离 |
| html-prototype-to-figma | prototype-delivery＋adapters/figma-delivery | 合并 Figma 交付流程 |
| figma-design-sync | prototype-delivery＋adapters/figma-delivery | 合并 Figma 修改与验证 |
| figma-mcp-troubleshooting | adapters | 按需排障，不复制官方 API 契约 |
| browser-automation | prototype-qa＋browser 适配 | 保留实际验证方法，不带入反爬规避 |
| prototype-share-bundle | prototype-delivery＋scripts/export | 修复资源与 PRD 完整性边界 |
| prd-export-docx | prototype-delivery＋scripts/export | Word 输出与内容验证 |
| full-output-enforcement | prototype-studio＋prototype-qa | 取消独立入口，交付必须完整且如实报告 |
| project-workspace-init | 包外原技能 | 只更新其原型规则模板 |

## 兼容边界

`v5-ux-rule` 保留同名短入口，仅把显式 V5 请求转交新设计实现与 V5 标准包。既有多个项目引用已不存在的 `html-prototype-style`，提供同名短入口转交原型工作室；不批量修改这些项目的业务规则。兼容入口没有旧资产、旧建档流程或第二套设计规范。

原项目的显式 Skill 调用限制继续适用。模板更新仅影响将来初始化；不改变已经存在的项目授权方式。新入口遵循当前用户请求及项目规则，不把迁移推定为其他项目的修改授权。

## 维护源

- 页面登记、PRD、数据含义、确认记录：项目内的规格文件。
- 共享业务记录：项目实际数据模块；统计从基础记录计算。
- 标准件规范、锁定文件和真实图片：选定标准包版本。
- 导航、PRD 阅读内容、性能确认表：从上述来源生成的阅读视图。

脚本验证和真实浏览器验收分别记录。它们不等于用户已评审，也不批准任何真实业务数据。
