# 🧠 Prophet Sentinel - AI Risk Guardian for DeFi

> **中文** | AI预言 + 隐私盾 + 即时警报，为DeFi用户提供链上风险防护  
> **English** | AI Prediction + Privacy Shield + Instant Alerts, providing on-chain risk protection for DeFi users

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.2-61DAFB.svg)](https://reactjs.org/)
[![Solana](https://img.shields.io/badge/solana-web3.js-9945FF.svg)](https://solana.com/)

---

## 🎯 项目简介 | Project Overview

**中文：**  
Prophet Sentinel 是一个**AI驱动的DeFi风险预测系统**，专注于Solana生态。通过机器学习模型分析链上数据，实时预测协议风险，帮助用户在rug pull和闪崩前及时撤离。

**English:**  
Prophet Sentinel is an **AI-driven DeFi risk prediction system** focused on the Solana ecosystem. It analyzes on-chain data through machine learning models to predict protocol risks in real-time, helping users exit before rug pulls and flash crashes.

### 核心功能 | Key Features

- 🎯 **实时风险预测** | **Real-time Risk Prediction** - RandomForest模型输出0-100风险分数 | RandomForest model outputs 0-100 risk scores
- 🤖 **Telegram即时警报** | **Telegram Instant Alerts** - 高风险协议自动推送通知 | Auto-push notifications for high-risk protocols
- 🔒 **隐私保护分析** | **Privacy-Protected Analysis** - zk-proof验证，不泄露钱包地址 | zk-proof verification without revealing wallet addresses
- 🌱 **ESG绿色评分** | **ESG Green Rating** - 可持续性分析，推荐低能耗协议 | Sustainability analysis, recommending low-energy protocols
- 📊 **可视化热图** | **Visual Heatmap** - 直观展示多协议风险对比 | Intuitive multi-protocol risk comparison
- ⚡ **快速响应** | **Fast Response** - API响应时间 < 2秒 | API response time < 2 seconds

---

## 🏗️ 系统架构

```plaintext
┌─────────────────────────────┐
│   React前端Dashboard         │
│   - 风险热图                  │
│   - 协议详情卡片              │
│   - 实时数据刷新              │
└──────────┬──────────────────┘
           │ REST API
┌──────────▼──────────────────┐
│   Flask后端 + ML模型         │
│   - /predict_risk API        │
│   - RandomForest推理         │
│   - Solana数据拉取           │
│   - ESG计算模块              │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│   Telegram Bot (Node.js)     │
│   - /risk 命令查询           │
│   - 风险订阅推送              │
│   - 定时监控                 │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│   Solana Network            │
│   - Jupiter / Orca / Raydium│
│   - 链上指标实时拉取          │
└──────────────────────────────┘
```

---

## 🚀 快速开始 | Quick Start

### 前置要求 | Prerequisites

- Python 3.11+
- Node.js 18+
- npm/yarn
- Git

### 1. 克隆项目 | Clone Repository

```bash
git clone https://github.com/yourusername/prophet-sentinel.git
cd prophet-sentinel
```

### 2. 环境配置 | Environment Setup

**中文：** 复制环境变量模板并填写配置  
**English:** Copy environment template and fill in configuration

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# Flask配置
FLASK_SECRET_KEY=your-secret-key-here

# Solana配置
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=your-helius-api-key  # 可选

# Telegram配置
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### 3. 训练ML模型 | Train ML Model

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 训练模型（生成合成数据）| Train model (generate synthetic data)
python models/train_model.py
```

**输出示例 | Output Example:**
```
🚀 Prophet Sentinel - 模型训练开始
🔧 生成 2000 条合成训练数据...
✅ 数据生成完成: 2000 条记录
🤖 开始训练模型...
🎯 模型训练完成!
准确率: 87.50%
💾 模型已保存: backend/models/risk_model.pkl
```

### 4. 启动后端API | Start Backend API

```bash
# 在 backend/ 目录下 | In backend/ directory
python app.py
```

**中文：** 访问 http://localhost:5001 查看API文档  
**English:** Visit http://localhost:5001 for API documentation

### 5. 启动前端 | Start Frontend

```bash
cd frontend
npm install
npm start
```

**中文：** 访问 http://localhost:3000 查看Dashboard  
**English:** Visit http://localhost:3000 for Dashboard

### 6. 启动Telegram Bot（可选）| Start Telegram Bot (Optional)

```bash
cd telegram-bot
npm install
npm start
```

---

## 📡 API文档 | API Documentation

### 获取风险预测 | Get Risk Prediction

```http
GET /api/predict_risk?protocol=Jupiter
```

**响应示例 | Response Example:**
```json
{
  "protocol": "Jupiter",
  "risk_score": 45,
  "alert_level": "medium",
  "alert_emoji": "⚡",
  "sustainable_score": 92,
  "timestamp": "2025-10-23T12:00:00Z",
  "metrics": {
    "volume_24h": 50000000,
    "liquidity_change": -0.08,
    "whale_transfers": 3,
    "holder_concentration": 0.52
  },
  "confidence": 0.87
}
```

### 获取支持的协议 | Get Supported Protocols

```http
GET /api/protocols
```

### 健康检查 | Health Check

```http
GET /api/health
```

### zk隐私验证 | zk Privacy Verification

```http
POST /api/verify_proof
Content-Type: application/json

{
  "wallet_hash": "abc123...",
  "risk_score": 75
}
```

---

## 🤖 Telegram Bot使用 | Telegram Bot Usage

### 可用命令 | Available Commands

| 命令 Command | 说明 Description | 示例 Example |
|--------------|------------------|--------------|
| `/start` | 开始使用 Start | `/start` |
| `/risk <协议>` | 查询风险 Query Risk | `/risk Jupiter` |
| `/protocols` | 协议列表 Protocol List | `/protocols` |
| `/subscribe` | 订阅警报 Subscribe Alerts | `/subscribe` |
| `/unsubscribe` | 取消订阅 Unsubscribe | `/unsubscribe` |
| `/help` | 帮助信息 Help Info | `/help` |

### 使用示例 | Usage Example

```
User: /risk Orca
Bot:  ⚡ Orca 风险分析

风险评分: 38/100
风险等级: MEDIUM
评估: 中等风险，谨慎使用

绿色评分: 88/100 🌿 较为环保

链上指标:
• 24h交易量: $28.50M
• 流动性变化: -5.2%
• 鲸鱼转移: 2次
• 持有集中度: 48.3%

更新时间: 2025-10-23 20:15:32
```

---

## 📊 技术栈 | Tech Stack

### 后端 | Backend
- **框架 Framework:** Flask 3.0
- **ML:** scikit-learn (RandomForest)
- **区块链 Blockchain:** solana-py, base58
- **数据处理 Data Processing:** pandas, numpy

### 前端 | Frontend
- **框架 Framework:** React 18.2
- **图表 Charts:** Recharts 2.10
- **HTTP:** axios
- **钱包 Wallet:** @solana/wallet-adapter (optional)

### Bot
- **框架 Framework:** Telegraf.js 4.15
- **定时任务 Cron:** node-cron
- **HTTP:** axios

---

## 🧪 测试 | Testing

### 后端测试 | Backend Testing

```bash
cd backend
pytest tests/
```

### API测试 | API Testing

```bash
# 测试风险预测 | Test risk prediction
curl "http://localhost:5001/api/predict_risk?protocol=Jupiter"

# 健康检查 | Health check
curl "http://localhost:5001/api/health"
```

### 前端测试 | Frontend Testing

```bash
cd frontend
npm test
```

---

## 📈 性能指标 | Performance Metrics

| 指标 Metric | 目标值 Target | 实际值 Actual |
|------|--------|--------|
| API响应时间 API Response | < 2s | ~1.5s |
| ML推理时间 ML Inference | < 100ms | ~80ms |
| 前端加载 Frontend Load | < 3s | ~2.2s |
| 模型准确率 Model Accuracy | ≥ 80% | 87.5% |

---

## 🛠️ 开发指南 | Development Guide

### 项目结构 | Project Structure

```
prophet-sentinel/
├── backend/                 # Flask后端
│   ├── app.py              # 主程序
│   ├── config.py           # 配置
│   ├── models/             # ML模型
│   │   ├── train_model.py
│   │   └── predict.py
│   ├── services/           # 业务逻辑
│   │   ├── solana_service.py
│   │   └── sustainability.py
│   └── utils/              # 工具函数
│
├── frontend/               # React前端
│   ├── src/
│   │   ├── components/    # React组件
│   │   ├── services/      # API调用
│   │   └── App.js
│   └── public/
│
├── telegram-bot/          # Telegram Bot
│   ├── bot.js
│   └── commands/
│
├── data/                  # 数据文件
│   ├── raw/
│   └── processed/
│
├── tests/                 # 测试文件
├── docs/                  # 文档
└── scripts/              # 部署脚本
```

### 添加新协议 | Add New Protocol

**中文：**
1. 更新 `backend/services/solana_service.py` 中的 `PROTOCOL_DATA`
2. 在前端 `RiskHeatmap.js` 的 `PROTOCOLS` 数组添加协议名

**English:**
1. Update `PROTOCOL_DATA` in `backend/services/solana_service.py`
2. Add protocol name to `PROTOCOLS` array in frontend `RiskHeatmap.js`

### 自定义ML模型 | Customize ML Model

**中文：** 修改 `backend/models/train_model.py`  
**English:** Modify `backend/models/train_model.py`

```python
# 调整模型参数
model = RandomForestClassifier(
    n_estimators=200,  # 增加树的数量
    max_depth=15,      # 增加深度
    random_state=42
)
```

---

## 🌱 ESG绿色评分 | ESG Green Rating

**中文：** Prophet Sentinel 是首个集成ESG分析的DeFi风险工具。  
**English:** Prophet Sentinel is the first DeFi risk tool integrating ESG analysis.

### 评分标准 | Rating Standards

- **90-100分 Score**: 🌟 非常环保 Very Eco-friendly
- **70-89分 Score**: 🌿 较为环保 Eco-friendly
- **50-69分 Score**: ⚡ 能耗中等 Medium Energy
- **0-49分 Score**: ⚠️ 高能耗 High Energy

### 计算公式

```python
energy_consumption = tx_count * 0.00051  # kWh (Solana PoH)
carbon_footprint = energy_consumption * 0.4  # kg CO2
sustainable_score = 100 - log_scale(carbon_footprint)
```

---

## 🔒 隐私保护 | Privacy Protection

### zk-proof验证（演示版）| zk-proof Verification (Demo)

```python
# 简化版实现 | Simplified implementation
proof_hash = sha256(wallet_address + risk_score + timestamp)
# 实际应使用 zk-SNARK / Semaphore | Should use zk-SNARK/Semaphore in production
```

### 数据安全 | Data Security

- ✅ 不存储用户钱包原始地址 | No storage of raw wallet addresses
- ✅ 不记录交易历史 | No transaction history logging
- ✅ API请求不携带身份信息 | API requests carry no identity info
- ✅ 可选匿名模式 | Optional anonymous mode

---

## 📦 部署 | Deployment

### Render部署（后端）| Render Deployment (Backend)

```bash
# render.yaml
services:
  - type: web
    name: prophet-sentinel-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

### Vercel部署（前端）| Vercel Deployment (Frontend)

```bash
cd frontend
npm run build
vercel --prod
```

### Railway部署（Telegram Bot）| Railway Deployment (Bot)

```bash
cd telegram-bot
# 连接GitHub自动部署 | Connect GitHub for auto-deployment
```

---

## 🤝 贡献指南 | Contributing

**中文：** 欢迎贡献！请遵循以下步骤：  
**English:** Contributions welcome! Please follow these steps:

1. Fork本仓库 | Fork the repository
2. 创建功能分支 | Create feature branch (`git checkout -b feature/AmazingFeature`)
3. 提交更改 | Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 | Push to branch (`git push origin feature/AmazingFeature`)
5. 开启Pull Request | Open a Pull Request

---

## 📝 更新日志 | Changelog

### v1.0.0 (2025-10-23)

- ✅ 实现RandomForest风险预测模型 | Implemented RandomForest risk prediction model
- ✅ Flask后端API | Flask backend API
- ✅ React可视化Dashboard | React visualization Dashboard
- ✅ Telegram Bot警报系统 | Telegram Bot alert system
- ✅ ESG绿色评分 | ESG green rating
- ✅ zk隐私验证（演示版）| zk privacy verification (demo)

---

## 🐛 已知问题 | Known Issues

- [ ] Solana RPC可能有速率限制（建议使用Helius）| Solana RPC may have rate limits (recommend using Helius)
- [ ] zk-proof为简化实现（生产环境需集成真实zk库）| zk-proof is simplified (production needs real zk library)
- [ ] 前端钱包连接功能待完善 | Frontend wallet connection to be improved

---

## 📚 参考资料 | References

- [Solana Documentation](https://docs.solana.com/)
- [scikit-learn Guide](https://scikit-learn.org/stable/user_guide.html)
- [Telegraf.js Documentation](https://telegraf.js.org/)
- [Recharts Examples](https://recharts.org/en-US/examples)

---

## 📄 License | 许可证

**English:** This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details  
**中文：** 本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 💡 致谢 | Acknowledgments

**中文：**
- Solana Foundation - 提供高性能区块链基础设施
- Helius - Solana数据API支持
- DeFi社区 - 激励我们构建更安全的工具

**English:**
- Solana Foundation - High-performance blockchain infrastructure
- Helius - Solana data API support
- DeFi Community - Inspiring us to build safer tools

---

## 📧 联系方式 | Contact

- **Email:** yaow1211@gmail.com
- **X / Twitter:** [@MiaStarsAlign](https://twitter.com/MiaStarsAlign)
- **Telegram:** [@MiaStarsAlign](https://t.me/MiaStarsAlign)

---

**⚡ 在DeFi丛林，让Prophet Sentinel成为你的数据哨兵！**  
**⚡ In the DeFi jungle, let Prophet Sentinel be your data sentinel!**





