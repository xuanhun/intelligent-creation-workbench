# 测试与交付

```shell
python scripts/check.py --out test-runs/core-01
python scripts/check.py --with-api --out test-runs/api-01
```

第二条要求安装 `.[dev]`。基础模式不导入 API，报告列出未执行检查。输出目录必须不存在，失败日志不覆盖。脚本从任意工作目录定位根目录，保存实际命令、stdout/stderr、退出码、耗时、Python、Git HEAD、输入 SHA256 与输入是否变化。

Web：在 `web` 执行 `npm ci`、`npm run build`。包：根目录 `python -m build`，安装 wheel 至新 venv，在仓库外 `python -I -c "import creation_workbench; print(creation_workbench.__version__)"`。API 测试使用 httpx ASGITransport，不访问外部服务。

CI 基础检查覆盖 Windows/Linux Python 3.11–3.14；API/包验证和 Node 24 Web 构建独立执行，保存检查产物。配置不是实际远程运行证据。

G0 另行记录 SDK、Runtime、模型、网关版本与配置哈希，保存脱敏 SSE、call_id 往返、历史恢复、错误、取消与重复回调证据。模拟任务不替代真实模型。发布另行审计迁移、隔离、许可证和部署，本轮不包含发布或推送。
