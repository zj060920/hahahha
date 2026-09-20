# AI Hardware Market Monitor — A股+美股 MCP/Codex Plugin

研究型 A 股 + 美股 AI 硬件行情监控插件。

功能：A股公开行情/K线、美股 Yahoo Finance、1m/5m/15m/30m/60m/日线、MACD/RSI/MA/ATR/OBV/成交量比、支撑阻力、CPO/PCB/存储联动、MACD/MA/RSI回测、风险检查、新闻检索、每日简报、MCP工具、Codex manifest、GitHub Actions。

> 公开行情源可能延迟、限流或不可用。本项目用于研究和技术分析，不是交易所级实时行情，也不是投资建议。

## 一键上传 GitHub

解压后：

Windows PowerShell:
```powershell
gh auth login
.\push_to_github.ps1
```

macOS/Linux:
```bash
gh auth login
chmod +x push_to_github.sh
./push_to_github.sh
```

默认仓库：https://github.com/zj060920/hahahha.git

GitHub 网页上传时必须先解压 ZIP。

## MCP 工具

`quote_tool`、`technical_analysis`、`compare_symbols`、`sector_linkage`、`strategy_backtest`、`risk_manager_tool`、`screen_stock`、`news_impact`、`daily_market_brief`
