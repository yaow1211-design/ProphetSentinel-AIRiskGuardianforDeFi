# 🛠️ Prophet Sentinel - 技术栈详解

**更新时间：** 2025-10-22

---

## 📚 技术选型理由

### 为什么选择这些技术？

| 技术 | 选择理由 | 替代方案 |
|------|----------|----------|
| **Python + scikit-learn** | ML原型快速开发，生态成熟 | TensorFlow (过重) |
| **Flask** | 轻量级，适合MVP，易部署 | FastAPI (可选升级) |
| **React** | 前端生态最成熟，组件丰富 | Vue/Svelte |
| **Telegraf.js** | Telegram Bot最佳框架 | python-telegram-bot |
| **Recharts** | React原生图表库，易用 | D3.js (太复杂) |
| **Solana Web3.js** | Solana官方SDK | Anchor (过重) |

---

## 🎨 架构设计原则

### 1. 模块化设计
```
每个模块独立运行，通过API通信
✅ 易于测试和调试
✅ 可单独部署和扩展
✅ 降低耦合度
```

### 2. 渐进式增强
```
MVP核心功能 → 高级功能 → 优化
Day 1-5: 基础功能可用
Day 6-8: 高级功能演示
Day 9-10: 打磨和优化
```

### 3. 数据流设计
```
Solana区块链 → Flask API → ML模型 → 前端展示
                  ↓
            Telegram Bot推送
```

---

## 🔧 完整技术栈清单

### 后端 (Python)

```python
# requirements.txt
flask==3.0.0              # Web框架
flask-cors==4.0.0         # 跨域支持
gunicorn==21.2.0          # 生产服务器

# ML/数据处理
scikit-learn==1.3.2       # ML模型
pandas==2.1.3             # 数据处理
numpy==1.26.2             # 数值计算
joblib==1.3.2             # 模型序列化

# Solana集成
solana==0.30.2            # Solana SDK
base58==2.1.1             # 地址编码

# 工具库
python-dotenv==1.0.0      # 环境变量
requests==2.31.0          # HTTP请求
redis==5.0.1              # 缓存（可选）
```

**关键依赖说明：**
- `scikit-learn`: RandomForest模型训练
- `solana`: 链上数据查询
- `flask-cors`: 允许前端跨域请求

---

### 前端 (React)

```json
// package.json dependencies
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  
  // 图表
  "recharts": "^2.10.0",
  "chart.js": "^4.4.0",
  
  // Solana钱包
  "@solana/wallet-adapter-react": "^0.15.35",
  "@solana/wallet-adapter-react-ui": "^0.9.35",
  "@solana/wallet-adapter-wallets": "^0.19.32",
  "@solana/web3.js": "^1.87.6",
  
  // 工具
  "axios": "^1.6.2",
  "dotenv": "^16.3.1",
  "tailwindcss": "^3.3.5"  // 可选：样式框架
}
```

**关键依赖说明：**
- `recharts`: 响应式图表库，适合风险热图
- `@solana/wallet-adapter-*`: Phantom钱包集成
- `tailwindcss`: 快速构建现代UI（可选）

---

### Telegram Bot (Node.js)

```json
// telegram-bot/package.json
{
  "telegraf": "^4.15.0",     // Bot框架
  "axios": "^1.6.2",         // API调用
  "dotenv": "^16.3.1",       // 环境变量
  "node-cron": "^3.0.3"      // 定时任务（推送）
}
```

---

### 开发工具

```bash
# Python开发工具
pip install black           # 代码格式化
pip install pylint          # 代码检查
pip install pytest          # 测试框架

# Node.js开发工具
npm install -D eslint       # JS代码检查
npm install -D prettier     # 代码格式化
```

---

## 🗂️ 推荐项目结构

```
prophet-sentinel/
│
├── backend/                          # Python后端
│   ├── app.py                        # Flask主程序
│   ├── config.py                     # 配置管理
│   ├── requirements.txt
│   │
│   ├── models/                       # ML模型
│   │   ├── train_model.py           # 训练脚本
│   │   ├── predict.py               # 推理逻辑
│   │   └── risk_model.pkl           # 训练好的模型
│   │
│   ├── services/                     # 业务逻辑
│   │   ├── solana_service.py        # Solana数据拉取
│   │   ├── alert_service.py         # 警报推送
│   │   ├── zk_privacy.py            # 隐私验证
│   │   └── sustainability.py        # ESG计算
│   │
│   ├── routes/                       # API路由
│   │   ├── risk_routes.py
│   │   └── health_routes.py
│   │
│   └── utils/                        # 工具函数
│       ├── cache.py
│       └── logger.py
│
├── frontend/                         # React前端
│   ├── public/
│   ├── src/
│   │   ├── components/              # React组件
│   │   │   ├── RiskHeatmap.jsx
│   │   │   ├── WalletConnect.jsx
│   │   │   ├── AlertPanel.jsx
│   │   │   └── ESGScore.jsx
│   │   │
│   │   ├── services/                # API调用
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   └── index.js
│   │
│   └── package.json
│
├── telegram-bot/                     # Telegram Bot
│   ├── bot.js                        # Bot主程序
│   ├── commands/                     # 命令处理
│   │   ├── risk.js
│   │   └── subscribe.js
│   └── package.json
│
├── data/                             # 数据文件
│   ├── raw/                          # 原始数据
│   ├── processed/                    # 处理后数据
│   └── generate_synthetic_data.py   # 合成数据脚本
│
├── notebooks/                        # Jupyter实验
│   └── model_exploration.ipynb
│
├── tests/                            # 测试文件
│   ├── test_api.py
│   ├── test_model.py
│   └── test_solana.py
│
├── scripts/                          # 部署脚本
│   ├── deploy_backend.sh
│   └── deploy_frontend.sh
│
├── docs/                             # 文档
│   ├── API.md                        # API文档
│   └── ARCHITECTURE.md               # 架构说明
│
├── .env.example                      # 环境变量模板
├── .gitignore
├── README.md
├── PRD.md
├── DEVELOPMENT_PLAN.md
└── TECH_STACK.md
```

---

## 🔐 环境变量配置

### .env.example
```bash
# Flask配置
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-here
PORT=5000

# Solana配置
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_NETWORK=mainnet-beta
HELIUS_API_KEY=your-helius-api-key

# Telegram配置
TELEGRAM_BOT_TOKEN=your-bot-token-here
TELEGRAM_ADMIN_CHAT_ID=your-chat-id

# Redis缓存（可选）
REDIS_URL=redis://localhost:6379

# 前端配置
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SOLANA_NETWORK=mainnet-beta
```

---

## 🚀 快速启动命令

### 1. 后端启动
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 2. 前端启动
```bash
cd frontend
npm install
npm start
```

### 3. Telegram Bot启动
```bash
cd telegram-bot
npm install
node bot.js
```

### 4. 全栈启动（推荐使用tmux/screen）
```bash
# 终端1: 后端
cd backend && python app.py

# 终端2: 前端
cd frontend && npm start

# 终端3: Bot
cd telegram-bot && node bot.js
```

---

## 📊 性能基准

### 目标性能指标

| 指标 | 目标值 | 测试方法 |
|------|--------|----------|
| API响应时间 | < 2秒 | `curl -w "@curl-format.txt"` |
| ML推理时间 | < 100ms | `time.time()` 计时 |
| 前端首屏加载 | < 3秒 | Chrome DevTools |
| Telegram响应 | < 2秒 | 手动测试 |
| 并发处理 | 100 req/s | Apache Bench |

### 性能测试脚本
```bash
# API压力测试
ab -n 1000 -c 10 http://localhost:5000/api/predict_risk?protocol=Jupiter

# 前端性能分析
npm run build
npx serve -s build
# 使用 Lighthouse 测试
```

---

## 🔒 安全考虑

### 1. API安全
- ✅ 添加rate limiting（防止滥用）
- ✅ 验证输入参数
- ✅ HTTPS部署（生产环境）
- ✅ API key认证（可选）

### 2. 隐私保护
- ✅ 不存储钱包原始地址
- ✅ 使用hash处理敏感数据
- ✅ zk-proof验证（演示版）

### 3. 错误处理
```python
# 全局错误处理
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({
        'error': str(e),
        'status': 'error'
    }), 500
```

---

## 📦 部署方案

### 推荐部署平台

| 组件 | 推荐平台 | 免费额度 | 部署难度 |
|------|----------|----------|----------|
| Flask后端 | Render/Railway | ✅ 有 | ⭐ 简单 |
| React前端 | Vercel/Netlify | ✅ 有 | ⭐ 极简 |
| Telegram Bot | Railway/Heroku | ✅ 有 | ⭐⭐ 中等 |
| 数据库 | Supabase/MongoDB Atlas | ✅ 有 | ⭐ 简单 |

### 快速部署步骤

#### 后端部署到Render
```bash
# 1. 创建 render.yaml
services:
  - type: web
    name: prophet-sentinel-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0

# 2. 连接GitHub仓库
# 3. 自动部署
```

#### 前端部署到Vercel
```bash
# 1. 安装Vercel CLI
npm i -g vercel

# 2. 部署
cd frontend
vercel --prod
```

---

## 🧪 测试策略

### 测试金字塔

```
        /\
       /UI\         E2E测试（少量）
      /____\
     /      \
    /Integration\   集成测试（中量）
   /____________\
  /              \
 /  Unit Tests    \  单元测试（大量）
/__________________\
```

### 关键测试用例

1. **ML模型测试**
```python
def test_model_prediction():
    metrics = {
        'volume_24h': 1000000,
        'liquidity_change': -0.2,
        'whale_transfers': 5,
        'holder_concentration': 0.8
    }
    result = predict_risk(metrics)
    assert 0 <= result['risk_score'] <= 100
```

2. **API测试**
```python
def test_predict_risk_endpoint():
    response = client.get('/api/predict_risk?protocol=Jupiter')
    assert response.status_code == 200
    assert 'risk_score' in response.json
```

3. **前端测试**
```javascript
test('renders risk heatmap', () => {
  render(<RiskHeatmap />);
  expect(screen.getByText('风险热图')).toBeInTheDocument();
});
```

---

## 📈 监控和日志

### 推荐工具
- **日志**: Python `logging` + 文件输出
- **监控**: Render/Railway内置监控
- **错误追踪**: Sentry (可选)

### 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 💰 成本估算

### 开发阶段（10天）
- ✅ 所有服务免费（使用Free Tier）
- ✅ Helius API免费额度足够
- ✅ Telegram Bot完全免费

### 生产环境（每月）
| 服务 | 成本 |
|------|------|
| Render (后端) | $0-7 |
| Vercel (前端) | $0 |
| Railway (Bot) | $0-5 |
| **总计** | **$0-12/月** |

---

## 🎓 学习资源

### 核心技术文档
- [Flask Quickstart](https://flask.palletsprojects.com/quickstart/)
- [scikit-learn Tutorial](https://scikit-learn.org/stable/tutorial/)
- [React Docs](https://react.dev/learn)
- [Solana Cookbook](https://solanacookbook.com/)
- [Telegraf Guide](https://telegraf.js.org/)

### 推荐视频教程
- Flask API开发: YouTube "Python Flask Tutorial"
- React + Solana: "Solana dApp Development"
- ML入门: Coursera "Machine Learning" (吴恩达)

---

## ✅ 开发检查清单

### 环境准备
- [ ] Python 3.11+ 已安装
- [ ] Node.js 18+ 已安装
- [ ] Git 已配置
- [ ] VS Code + 插件已安装
- [ ] Telegram账号已创建Bot

### 第一天任务
- [ ] 创建项目目录
- [ ] 初始化Git仓库
- [ ] 安装所有依赖
- [ ] 配置.env文件
- [ ] 测试基础环境

---

**准备好了吗？开始编码吧！🚀**



