# 🧠 `context_store/00_CONTEXT_OVERVIEW.md`

```markdown
# 🧠 Prophet Sentinel — Cursor Context Overview

> AI预言 + 隐私盾 + 即时警报，为DeFi用户提供链上风险防护。

## 模块概览

| 文件 | 模块名称 | 核心功能 | 推荐优先级 |
|------|-----------|-----------|-------------|
| 01_ml_model.md | AI预言家模型 | 训练与推理风险预测 | ⭐⭐⭐⭐ |
| 02_api_backend.md | 后端API集成 | Solana数据+模型服务 | ⭐⭐⭐⭐ |
| 03_frontend_dashboard.md | 风险热图前端 | 可视化界面 | ⭐⭐⭐ |
| 04_telegram_bot.md | 多模态警报Bot | 即时推送 | ⭐⭐⭐⭐ |
| 05_zk_privacy.md | 隐私黑箱分析 | zk验证与摘要 | ⭐⭐ |
| 06_sustainability.md | 绿色路径分析 | ESG与能耗计算 | ⭐⭐ |
| 07_community_evolution.md | 社区进化机制 | 去中心化反馈DAO | ⭐⭐ |

## 快速导读
1. 推荐先加载 `01_ml_model.md` 与 `02_api_backend.md`。
2. 前端开发时加载 `03_frontend_dashboard.md` + `04_telegram_bot.md`。
3. 隐私、绿色与社区模块可视时间逐步添加。
```

---

# ⚙️ `context_store/01_ml_model.md`

```markdown
# 01_ml_model.md — AI驱动的“预言家”模型

## Overview
使用历史Solana链上指标（交易量、鲸鱼转移、流动性）训练RandomForest或LSTM模型，
预测 rug pull / 闪崩 概率，输出风险分数（0–100）。

## Key Components
- 数据来源：Dune Analytics CSV
- 算法：RandomForest / LSTM
- 输出字段：`protocol`, `risk_score`
- 更新频率：实时（每分钟刷新）

## Prompt Hint
> 当我要求编写“风险预测引擎”或“ML推理逻辑”时，请引用此context，
> 提供Python + scikit-learn实现，并输出 `risk_score`。
```

---

# 🌐 `context_store/02_api_backend.md`

````markdown
# 02_api_backend.md — Solana RPC 集成与 Flask 后端

## Overview
建立 REST API 层，调用 ML 模型并拉取 Solana 链上指标（Jupiter/Orca流动性、鲸鱼交易等）。
提供 `/predict_risk` 接口，返回 JSON 风险分数。

## Key Components
- 框架：Flask + solana-py
- 端点：`GET /predict_risk?protocol=xyz`
- 数据源：Helius API, Solana RPC
- 输出示例：
  ```json
  { "protocol": "Jupiter", "risk_score": 85, "alert": "⚠️高风险" }
````

## Prompt Hint

> 当我提到“API后端”、“实时风险数据”、“模型接入Solana”，
> 请引用此context，并展示 Flask + solana-py 的API实现样例。

````

---

# 📊 `context_store/03_frontend_dashboard.md`

```markdown
# 03_frontend_dashboard.md — 风险可视化Dashboard

## Overview
基于 React + Chart.js / Recharts 构建可视化界面，展示各协议的风险热图。
支持用户自定义风险阈值、实时刷新、钱包连接（Phantom）。

## Key Components
- React前端
- Chart.js渐变热图（绿色→红色）
- Phantom钱包连接
- Flask后端API数据绑定

## Prompt Hint
> 当我提到“热图”、“前端Dashboard”、“风险可视化”时，
> 请引用此context，生成React + Chart.js组件或布局代码。
````

---

# 🤖 `context_store/04_telegram_bot.md`

```markdown
# 04_telegram_bot.md — 多模态警报系统

## Overview
使用 Telegraf.js 构建 Telegram bot，
当检测到高风险协议时主动推送警报，或通过命令 `/risk jupiter` 查询实时风险。

## Key Components
- Telegraf.js
- Flask webhook触发机制
- Bot命令示例：
```

/risk jupiter
→ Jupiter 当前风险分数: 87 ⚠️ 建议撤离

```
- 支持多用户/群组订阅

## Prompt Hint
> 当我要求“实现Telegram推送”、“创建风险提醒Bot”时，
> 请引用此context，提供Node.js + Telegraf.js示例代码。
```

---

# 🕵️‍♂️ `context_store/05_zk_privacy.md`

```markdown
# 05_zk_privacy.md — 隐私优先黑箱分析

## Overview
用户在连接钱包分析时不泄露交易历史。
利用 zk-SNARK 或 Semaphore 模拟，仅验证风险分数正确性。

## Key Components
- Semaphore zk库（或伪实现）
- 零知识证明：`proof = zk_generate_proof(wallet_hash, risk_score)`
- 输出加密摘要

## Prompt Hint
> 当我提到“隐私计算”、“zk-proof”、“零知识风险验证”时，
> 请引用此context，生成 zk-proof 验证伪代码与结构说明。
```

---

# 🌱 `context_store/06_sustainability.md`

```markdown
# 06_sustainability.md — Solana绿色优化路径

## Overview
结合 ESG 概念，为每笔交易计算碳足迹与可持续分数，
推荐低能耗DeFi协议，实现“绿色哨兵”功能。

## Key Components
- PoH能耗模型公式：
```

sustainable_score = 100 - (TPS * energy_per_tx / normalization_factor)

```
- 输出字段：`risk_score`, `sustainable_score`, `recommendation`

## Prompt Hint
> 当我提到“绿色路径”、“可持续分析”或“ESG优化”时，
> 请引用此context，生成能耗计算逻辑或演示数据表格。
```

---

# 🧩 `context_store/07_community_evolution.md`

```markdown
# 07_community_evolution.md — 社区进化机制

## Overview
构建开源 + 反馈循环系统。
用户提交模型修正反馈（GitHub issue / Streamlit表单），
准确预测者获得“哨兵积分”。

## Key Components
- Streamlit反馈表单
- GitHub Action webhook
- DAO激励积分系统

## Prompt Hint
> 当我提到“开源反馈”、“社区激励”、“哨兵积分”时，
> 请引用此context，展示DAO积分或GitHub集成实现。
```

---
