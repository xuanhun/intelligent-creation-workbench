# 需求与基础设施来源

- 用户指定的 [分享会话](https://chatgpt.com/share/6ae9c555-9d64-83e8-820d-39899398522f) 已读取，定位其中关联的完整方案。
- [完整技术方案快照](technical-proposal.md) 来自 [原始 Page](https://chatgpt.com/space/page_e99edc1694448191929c401a9ff2dda2)，包含 26 章设计；2026-11-03 通过授权 Page 工具读取。快照保留设计内容，不是当前能力声明。
- 基础设施参考 `C:/code/py-visactor/py-elk`：src 布局、会话入口、实现计划、机器索引、独立检查报告、跨平台 CI 和失败证据保留。未复制其应用算法、上游依赖或验收结论。
- 官方边界核对：[Codex SDK](https://learn.chatgpt.com/docs/codex-sdk)。真实 SDK 与 Runtime 尚未安装，固定版本和兼容性验收属于 G0-01。

[sources.json](sources.json) 保存快照 SHA256、读取日期与参考仓库 HEAD。核心检查校验快照字节；更新需求时保留来源与变更原因，不静默修改基线。
