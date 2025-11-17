# stock-qt.py

初始回测与实时建议项目模板（策略 C：周内多时空尺度 ML 信号，股票池/ETF，仅做多）。

结构说明：
- `data/`：数据缓存与增量更新（包含 `cache.sqlite` 的示例路径）
- `scripts/`：数据抓取、特征工程、训练与回测脚本
- `reports/`：回测/运行生成的 Markdown 报告（`latest.md`）
- `logs/`：运行日志，`latest.log` 覆盖模式
- `.venv/`：本地 Python 虚拟环境（不提交）

参见 `agent_prompt_final.md` 和 `strategy_c_long_only_detailed.md` 以获取策略定义与实现约定。
