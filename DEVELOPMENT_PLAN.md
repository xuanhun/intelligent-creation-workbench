# 开发路线

设计见 [方案快照](references/technical-proposal.md)，执行状态见 [机器计划](docs/iteration-plan.json) 与 [当前状态](docs/RELEASE_STATUS.md)。

| 阶段 | 交付 | 验收 |
| --- | --- | --- |
| B00 | 文档、包、合同、API 探针、Web 起始页、检查与 CI | 离线检查、API 检查、Web 构建、安装包验证 |
| G0 | Responses 网关、模型目录、固定 SDK/Runtime、工具与异步原型 | 真实工具往返、多步执行、会话恢复、错误与取消 |
| G1 | 账户项目、SSE、Run/Job、版本、文章配图与分析 | 可编辑文章、选区修改、重连、权限/幂等/预算 |
| G2 | SceneSpec、信息图、DeckSpec、可编辑 PPT 与真实预览 | 数据正确、对象编辑、无溢出、交付文件可用 |
| G3 | 视频时间轴、媒体 Worker、发布与指标回收 | 恢复取消、音画检查、发布幂等与对账 |
| G4 | 团队、技能、渠道、资源池与成本优化 | 隔离、升级回归、恢复演练与负载验收 |

下一轮为 [G0-01](docs/iterations/G0-01.md)。模型端点、凭证、部署环境与首批渠道尚未选定；真实集成验收依赖这些输入。
