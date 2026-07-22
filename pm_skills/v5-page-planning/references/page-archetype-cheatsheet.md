# 版式速查（页面规划用）

> **单一事实源 = v5-ux-rule `references/00-page-archetypes.md`。** 本表只为"规划阶段快速选版式"，
> 决策树/壳层结构以 v5-ux-rule 为准；二者冲突时**以 v5-ux-rule 为准**，并回来修订本表。

## 第 0 步：先定平台（mobile / desktop）

每页先标平台，来源优先级：项目 `v5-profile.md` 平台映射 → 用户交代（如"用户端 H5 全移动、管理后台桌面"）→ 问用户一次。**平台写进每页规划文档的「平台」字段**，下游 v5-ux-rule 照抄不改判。管理后台类默认 desktop。

## 选版式决策树（同 v5-ux-rule，两平台同一棵树，禁自创新版式）

```
这个页面……
├─ 产品/Agent 总入口、欢迎或概览页？           → 桌面 A 首页/门户 ｜ 移动 A-m 门户(TabBar)
├─ 只在对话中完成（含 AI 返回卡片/列表/详情卡）？ → 桌面 B 对话流    ｜ 移动 B-m 对话流
└─ 对话旁需常驻面板看详情/填表单？              → 桌面 C 抽屉（轻=1/3屏500，重=半屏720）｜ 移动 C-m 底部弹层
```

## 版式 → 壳层 → 线框起手式

| 版式 | v5-ux-rule 壳层 | 本技能线框起手式 | 何时用 |
|---|---|---|---|
| A 首页/门户 | `shell/home-portal.html` | `assets/wireframe-snippets/A-home-portal.html` | 桌面产品首页、Agent 总入口、概览落地页 |
| B 对话流 | `shell/chat-flow.html` | `assets/wireframe-snippets/B-chat-flow.html` | 桌面与 Agent 对话、所有 AI 返回卡片场景 |
| C 抽屉·1/3屏 500 | `shell/drawer.html` | `assets/wireframe-snippets/C-drawer.html` | 桌面对话旁看轻量详情 |
| C 抽屉·半屏 720 | `shell/drawer-half.html` | `assets/wireframe-snippets/C-drawer-half.html` | 桌面对话旁填复杂表单/重内容 |
| A-m 移动门户 | `shell-mobile/portal.html` | `assets/wireframe-snippets/Am-mobile-portal.html` | 移动首页、Agent 总览、TabBar 一级页 |
| B-m 移动对话流 | `shell-mobile/chat-flow.html` | `assets/wireframe-snippets/Bm-mobile-chat-flow.html` | 移动与 Agent 对话的一切场景 |
| C-m 移动底部弹层 | `shell-mobile/sheet.html`（--half/--action） | `assets/wireframe-snippets/Cm-mobile-sheet.html` | 移动对话旁详情/表单/多选/动作菜单 |

## 不是独立页面（规划时常见误判）

| 看起来像 | 实际归属 | 规划写法 |
|---|---|---|
| 列表页 | B 里 AI 返回的列表卡片 / C 抽屉内容 | 不单列页，写进某页"区域 × 内容" |
| 详情页 | B 的详情卡片 / C 抽屉内容 | 同上 |
| 空/错误/加载态 | 对应页面内的"态"（empty-state / toast） | 不单列页 |
| 后台配置/管理页 | 超出对话原型；优先用 C 抽屉承载表单 | 用 C 抽屉规划 |
