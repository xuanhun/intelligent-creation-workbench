# 智能创作工作台会话入口

先读 [NEW_SESSION](docs/NEW_SESSION.md)、[实现策略](docs/IMPLEMENTATION_PLAN.md)、[机器计划](docs/iteration-plan.json) 与 [当前状态](docs/RELEASE_STATUS.md)。需求依据为 [方案快照](references/technical-proposal.md)。

- 保留用户改动，先检查 `git status`；不自行提交、推送或部署。
- 文档使用中文；Python 3.11+、src 布局，React 前端在 `web`。
- 平台拥有业务事实；Codex Thread/Turn 仅描述执行，不替代 Run/Job/Artifact。
- 核心合同保持标准库可检查。外部 SDK 与 HTTP 依赖放适配层。
- 按真实闭环增加模块，禁止用空包数量或模拟执行冒充产品进展。
- 实现 SDK 前核对官方 API 与固定版本。模型、工具往返与恢复独立验收留证。
- 版本不可变；编辑绑定基础版本、对象与原文校验。可信租户、权限由后端注入。
- 长任务通过 Job 与持久事件推进；断连不取消 Run；发布绑定版本与实际授权。
- 每次检查使用新目录：`python scripts/check.py --out test-runs/<name>`；有 API 依赖加 `--with-api`。前端运行 `npm ci` 与 `npm run build`。
- 失败日志保留，修复后另起目录；跳过检查不得标为通过。
- 每轮更新状态、机器计划、变更记录与复盘，以实际证据声明完成。

基础设施借鉴 py-elk，不继承算法任务、上游锁或多 Agent 要求。并行 Agent 工作仅在用户明确要求时启用。
