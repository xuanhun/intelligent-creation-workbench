# 智能创作工作台

面向内容创作者的开源 AI 创作空间，覆盖资料、分析、文章、图片、信息图、PPT、视频与发布。采用 **Python 业务平台 + Codex Runtime + 自有模型网关 + 统一产物版本体系**。

当前为 **B00 项目初始化**：领域合同、Runtime 接口、FastAPI 探针、React 起始页、检查脚本与 CI。真实模型、数据库、后台任务与内容生成尚未接入；G0 未验收。详见 [当前状态](docs/RELEASE_STATUS.md)。

## 开始开发

CPython 3.11+，从仓库根目录执行，基础检查无需依赖、Node 或模型凭证：

```shell
python scripts/check.py --out test-runs/bootstrap-01
python examples/local_contracts.py
```

每次使用新输出目录；`report.json` 保存命令、退出码、日志与输入 SHA256。检查通过不代表 G0 或产品完成。

启动 API（本机开发）：

```shell
python -m venv .venv
# Windows PowerShell；Linux/macOS 使用 .venv/bin/python
.venv/Scripts/python -m pip install -e ".[dev]" -c requirements-dev.lock
.venv/Scripts/python -m uvicorn creation_workbench.api.app:app --reload --host 127.0.0.1
```

API 文档：<http://127.0.0.1:8000/docs>。`/health/live` 返回存活，`/health/ready` 在 Runtime 未接入时返回 503。API 检查：

```shell
.venv/Scripts/python scripts/check.py --with-api --out test-runs/api-01
```

另开终端启动 Web，要求 Node 22.12+，推荐 Node 24 LTS：

```shell
cd web
npm ci
npm run dev
```

访问 <http://127.0.0.1:5173>；开发代理将 `/api` 转发至本机 8000。起始页展示连接状态，尚不能发送创作任务。`npm run build` 执行类型检查和生产构建。

## 文档入口

- [新会话入口](docs/NEW_SESSION.md) 与 [协作约定](AGENTS.md)
- [完整方案快照](references/technical-proposal.md) 与 [来源记录](references/README.md)
- [架构与策略](docs/IMPLEMENTATION_PLAN.md)、[开发路线](DEVELOPMENT_PLAN.md)
- [机器计划](docs/iteration-plan.json)、[下一轮 G0-01](docs/iterations/G0-01.md)
- [测试与交付](docs/TEST_AND_RELEASE.md)、[配置](.env.example)、[基础服务规划](infrastructure/README.md)

基础设施参考 `C:/code/py-visactor/py-elk` 的文档入口、机器计划、独立检查收据与跨平台 CI；不继承 ELK 算法或完成声明。使用 [MIT 许可证](LICENSE)。
