---
name: ai-hardware-monitor
description: A股+美股 AI硬件行情、MACD多周期、CPO/PCB/存储联动和情景分析工作流。
---
# AI Hardware Monitor

实时/近期市场分析优先调用 MCP 获取数据，不凭记忆编造实时行情。

A股默认：CPO 300308/300502/300394；PCB 002916/002463/600183；存储 603986/301308/001309；半导体设备 688012/688072。
美股默认：LITE、COHR、ANET、MU、WDC、STX、SOXX、NVDA、AVGO。

分析：1m/5m/15m/30m/60m/日线 → MACD → RSI → MA → 成交量 → 支撑阻力 → 多周期共振 → CPO/PCB/存储联动 → 美股联动 → 情景与触发条件。
只做数据和情景分析，不把指标描述成确定性预测。
