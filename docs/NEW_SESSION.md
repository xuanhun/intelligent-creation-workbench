# 新会话入口

1. `git status --short`，检查本地改动和适用指令。
2. 阅读 [状态](RELEASE_STATUS.md)、[策略](IMPLEMENTATION_PLAN.md)、[机器计划](iteration-plan.json)。
3. 阅读 [G0-01 brief](iterations/G0-01.md) 和 [B00 复盘](retrospectives/B00.md)。
4. 从根目录执行 `python scripts/check.py --out test-runs/session-01`，每次换新目录。

当前 B00 提供开发基础设施与领域合同。真实 Codex、模型、存储、Worker、SSE 和内容生成均未实现。前端为起始工作区，API 只有只读探针。下一步核定 SDK/Runtime/模型版本组合并验证真实 Responses 工具循环。

目录：`src/creation_workbench/contracts`、`runtime_adapter`、`api`、`web`、`scripts`、`tests`、`references`、`infrastructure`。其他模块随实际闭环增加。
