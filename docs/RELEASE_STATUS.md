# 当前状态

B00 初始化已实现，版本 `0.0.1a0`，未正式发布。G0–G4 均未验收。

| 能力 | 状态 |
| --- | --- |
| 设计与入口 | 26 章方案快照、来源、路线、机器计划 |
| Python 合同 | 合法 Run 转换、冻结引用、基础选区校验 |
| Runtime | 只有 Protocol，无 SDK/模型连接 |
| API | 存活、未就绪与能力探针 |
| Web | 三栏起始页与 API 查询，无对话或编辑功能 |
| 检查 | 离线检查与可选 API 测试，保存日志与 SHA256 |
| CI | Windows/Linux Python 矩阵、API/包验证和 Web 构建配置 |
| 外部集成 | 模型、网关、数据库、Temporal、SSE、媒体、发布均未实现 |

本轮本机验证见 [B00 记录](changes/20261103-B00.json)。原始日志在被 Git 忽略的 `test-runs`。CI 尚需提交后运行，配置存在不表示远程通过。`BOOTSTRAP_CHECKS_PASS` 仅覆盖指定检查，不代表产品或 G0 验收。
