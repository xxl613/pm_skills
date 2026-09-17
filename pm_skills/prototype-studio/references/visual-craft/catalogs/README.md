# 本地设计查询资料

保留ui-ux-pro-max实际CSV与BM25脚本。运行 `python3 scripts/design/search.py "form validation" --domain ux --json`，或按当前工程选择 `--stack react` / `html-tailwind` / `vue` / `react-native` 等；不固定C端或React Native。

结果是可检索候选，不自动成为需求/标准。旧资料可能含偏好、阈值、历史库信息和示例数据；按平台/项目和当前资料判断，不能把候选色板、随机数或示例文案写成业务事实。

`--design-system`只用于无既定体系时辅助比较，`--persist`仅写显式指定的设计探索目录，不能覆盖项目DESIGN或指定标准件。无需联网、无需初始化新工程。
