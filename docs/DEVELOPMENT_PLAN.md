# 🚀 Prophet Sentinel - 10天开发计划

**制定时间：** 2025-10-22  
**目标完成日期：** 2025-10-30  
**策略：** MVP优先 + 核心功能完整 + 高级功能演示

---

## 📊 项目复杂度分析

### 依赖关系图
```
数据准备 → ML模型训练 → 后端API → 前端Dashboard
                           ↓
                    Telegram Bot
                           ↓
                    高级功能(zk/ESG)
```

### 优先级矩阵

| 模块 | 重要性 | 复杂度 | MVP必需 | 开发时间 |
|------|--------|--------|---------|----------|
| ML模型 | ⭐⭐⭐⭐⭐ | 🔴🔴🔴 | ✅ | 2天 |
| Flask后端 | ⭐⭐⭐⭐⭐ | 🔴🔴 | ✅ | 1.5天 |
| Telegram Bot | ⭐⭐⭐⭐ | 🔴 | ✅ | 1天 |
| React前端 | ⭐⭐⭐⭐ | 🔴🔴 | ✅ | 1.5天 |
| zk隐私验证 | ⭐⭐ | 🔴🔴🔴 | ❌ | 1天(伪实现) |
| ESG绿色评分 | ⭐⭐⭐ | 🔴 | ❌ | 0.5天 |
| 社区反馈 | ⭐⭐ | 🔴 | ❌ | 0.5天 |

---

## 🗓️ 详细开发时间表

### 📅 **阶段1: 项目基础搭建** (Day 1: 10/22, 4小时)

**目标：** 建立开发环境和项目结构

#### 任务清单：
- [x] 创建项目目录结构
```
prophet-sentinel/
├── backend/               # Flask后端
│   ├── app.py
│   ├── models/           # ML模型
│   ├── services/         # Solana集成
│   └── requirements.txt
├── frontend/             # React前端
│   ├── src/
│   ├── public/
│   └── package.json
├── telegram-bot/         # Telegram Bot
│   ├── bot.js
│   └── package.json
├── data/                 # 数据文件
│   ├── raw/
│   └── processed/
├── notebooks/            # Jupyter实验
└── docs/                 # 文档
```

- [ ] 安装Python依赖
```bash
# backend/requirements.txt
flask==3.0.0
flask-cors==4.0.0
solana==0.30.2
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
requests==2.31.0
python-dotenv==1.0.0
```

- [ ] 安装Node.js依赖
```bash
# telegram-bot/package.json
telegraf
dotenv
axios
```

- [ ] 配置环境变量模板
```bash
# .env.example
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
FLASK_SECRET_KEY=your_secret
```

**输出：** 完整项目骨架 + 依赖安装完成

---

### 📅 **阶段2: 数据准备** (Day 1-2: 10/22-10/23, 6小时)

**目标：** 获取并清洗训练数据

#### 任务清单：

1. **获取历史数据**
   - [ ] 从Dune Analytics下载Solana DeFi历史数据
   - [ ] 目标指标：
     - 日交易量 (volume_24h)
     - 流动性变化 (liquidity_change_pct)
     - 鲸鱼转移数量 (whale_transfers)
     - Token持有集中度 (gini_coefficient)
     - 历史rug pull标签 (is_rug_pull: 0/1)
   
2. **构建合成数据集**（如果Dune数据不足）
   ```python
   # data/generate_synthetic_data.py
   import pandas as pd
   import numpy as np
   
   # 生成100个协议的模拟历史数据
   protocols = ['Jupiter', 'Orca', 'Raydium', ...]
   # 特征: volume, liquidity, whale_activity, holder_concentration
   # 标签: risk_level (0=safe, 1=risky, 2=rug)
   ```

3. **数据清洗与特征工程**
   - [ ] 处理缺失值
   - [ ] 标准化数值特征
   - [ ] 创建衍生特征（如7日移动平均）
   - [ ] 划分训练/测试集 (80/20)

**输出：** `data/processed/training_data.csv`

---

### 📅 **阶段3: ML模型开发** (Day 2-3: 10/23-10/24, 8小时)

**目标：** 训练并验证风险预测模型

#### 任务清单：

1. **模型训练脚本**
```python
# backend/models/train_model.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

# 加载数据
df = pd.read_csv('data/processed/training_data.csv')
X = df[['volume_24h', 'liquidity_change', 'whale_transfers', 'holder_concentration']]
y = df['risk_level']

# 训练模型
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# 保存模型
with open('backend/models/risk_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# 验证准确率
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2%}")
```

2. **推理脚本**
```python
# backend/models/predict.py
def predict_risk(protocol_metrics):
    """
    输入: {'volume_24h': 1000000, 'liquidity_change': -0.15, ...}
    输出: {'risk_score': 85, 'risk_level': 'high'}
    """
    model = load_model()
    proba = model.predict_proba([metrics])[0]
    risk_score = int(proba[1] * 100)  # 0-100分
    return {'risk_score': risk_score}
```

3. **模型验证**
   - [ ] 在测试集上验证准确率 ≥ 75%
   - [ ] 测试边界情况
   - [ ] 性能基准测试（推理时间 < 100ms）

**输出：** `backend/models/risk_model.pkl` + 验证报告

---

### 📅 **阶段4: Flask后端开发** (Day 3-4: 10/24-10/25, 8小时)

**目标：** 实现REST API和Solana数据集成

#### 任务清单：

1. **核心API实现**
```python
# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.predict import predict_risk
from services.solana_service import get_protocol_metrics

app = Flask(__name__)
CORS(app)

@app.route('/api/predict_risk', methods=['GET'])
def api_predict_risk():
    protocol = request.args.get('protocol', 'Jupiter')
    
    # 1. 从Solana拉取实时指标
    metrics = get_protocol_metrics(protocol)
    
    # 2. ML模型预测
    prediction = predict_risk(metrics)
    
    # 3. 计算ESG分数（简化版）
    sustainable_score = calculate_sustainability(metrics)
    
    return jsonify({
        'protocol': protocol,
        'risk_score': prediction['risk_score'],
        'alert_level': get_alert_level(prediction['risk_score']),
        'sustainable_score': sustainable_score,
        'timestamp': datetime.utcnow().isoformat(),
        'metrics': metrics
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

2. **Solana数据服务**
```python
# backend/services/solana_service.py
from solana.rpc.api import Client
import requests

HELIUS_API = "https://api.helius.xyz/v0"

def get_protocol_metrics(protocol_name):
    """
    从Solana RPC + Helius API获取实时指标
    """
    # 简化版：使用模拟数据 + 真实RPC混合
    solana_client = Client("https://api.mainnet-beta.solana.com")
    
    # 拉取Jupiter/Orca等协议的TVL和交易量
    # （实际实现需要调用各协议的program ID）
    
    return {
        'volume_24h': fetch_24h_volume(protocol_name),
        'liquidity_change': fetch_liquidity_change(protocol_name),
        'whale_transfers': count_whale_transfers(protocol_name),
        'holder_concentration': calculate_gini(protocol_name)
    }
```

3. **API测试**
   - [ ] 使用Postman/curl测试所有端点
   - [ ] 验证响应时间 < 2秒
   - [ ] 添加错误处理和日志

**输出：** 可运行的Flask API服务

---

### 📅 **阶段5: React前端开发** (Day 4-5: 10/25-10/26, 10小时)

**目标：** 实现风险热图可视化Dashboard

#### 任务清单：

1. **项目初始化**
```bash
npx create-react-app frontend
cd frontend
npm install recharts @solana/wallet-adapter-react @solana/wallet-adapter-wallets
npm install axios dotenv
```

2. **核心组件开发**

```jsx
// frontend/src/components/RiskHeatmap.jsx
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import axios from 'axios';

function RiskHeatmap() {
  const [protocols, setProtocols] = useState([]);
  
  useEffect(() => {
    const fetchRisks = async () => {
      const protocolList = ['Jupiter', 'Orca', 'Raydium', 'Serum'];
      const results = await Promise.all(
        protocolList.map(p => 
          axios.get(`http://localhost:5000/api/predict_risk?protocol=${p}`)
        )
      );
      setProtocols(results.map(r => r.data));
    };
    
    fetchRisks();
    const interval = setInterval(fetchRisks, 30000); // 每30秒刷新
    return () => clearInterval(interval);
  }, []);
  
  const getColor = (score) => {
    if (score < 30) return '#22c55e'; // 绿色
    if (score < 70) return '#eab308'; // 黄色
    return '#ef4444'; // 红色
  };
  
  return (
    <div className="heatmap-container">
      <h2>🔥 DeFi协议风险热图</h2>
      <BarChart width={800} height={400} data={protocols}>
        <XAxis dataKey="protocol" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Bar dataKey="risk_score">
          {protocols.map((entry, index) => (
            <Cell key={index} fill={getColor(entry.risk_score)} />
          ))}
        </Bar>
      </BarChart>
    </div>
  );
}
```

3. **Phantom钱包集成**
```jsx
// frontend/src/components/WalletConnect.jsx
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';

function WalletConnect() {
  return (
    <div className="wallet-section">
      <WalletMultiButton />
      <p>连接钱包后可分析个人持仓风险</p>
    </div>
  );
}
```

4. **UI设计**
   - [ ] 现代化配色方案（深色主题）
   - [ ] 响应式布局
   - [ ] 加载动画和错误提示
   - [ ] 实时刷新指示器

**输出：** 可用的React Dashboard

---

### 📅 **阶段6: Telegram Bot开发** (Day 6: 10/26, 6小时)

**目标：** 实现即时风险警报系统

#### 任务清单：

1. **Bot核心逻辑**
```javascript
// telegram-bot/bot.js
const { Telegraf } = require('telegraf');
const axios = require('axios');
require('dotenv').config();

const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN);
const API_BASE = 'http://localhost:5000/api';

// 命令: /risk <协议名>
bot.command('risk', async (ctx) => {
  const protocol = ctx.message.text.split(' ')[1] || 'Jupiter';
  
  try {
    const response = await axios.get(`${API_BASE}/predict_risk?protocol=${protocol}`);
    const data = response.data;
    
    let emoji = '✅';
    if (data.risk_score > 70) emoji = '🚨';
    else if (data.risk_score > 40) emoji = '⚠️';
    
    ctx.reply(
      `${emoji} ${protocol} 风险分析\n\n` +
      `风险分数: ${data.risk_score}/100\n` +
      `警报等级: ${data.alert_level}\n` +
      `绿色评分: ${data.sustainable_score}\n` +
      `更新时间: ${new Date(data.timestamp).toLocaleString()}`
    );
  } catch (error) {
    ctx.reply('❌ 查询失败，请稍后重试');
  }
});

// 订阅高风险推送
bot.command('subscribe', (ctx) => {
  // 存储chat_id到数据库
  ctx.reply('✅ 已订阅高风险警报！风险分数>80时会自动推送');
});

bot.launch();
console.log('🤖 Telegram Bot 已启动');
```

2. **主动推送机制**
```python
# backend/services/alert_service.py
import requests

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def send_alert(chat_id, protocol, risk_score):
    message = f"🚨 高风险警报！\n\n{protocol}当前风险分数: {risk_score}\n建议立即检查持仓"
    
    requests.post(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
        json={'chat_id': chat_id, 'text': message}
    )
```

3. **测试**
   - [ ] 在Telegram创建测试Bot
   - [ ] 测试所有命令
   - [ ] 验证推送延迟 < 2秒

**输出：** 可运行的Telegram Bot

---

### 📅 **阶段7: 高级功能** (Day 7: 10/27, 6小时)

**目标：** 实现zk隐私验证和ESG评分（演示版）

#### 任务清单：

1. **zk隐私验证（伪实现）**
```python
# backend/services/zk_privacy.py
import hashlib

def generate_proof(wallet_address, risk_score):
    """
    简化版zk-proof生成
    实际应使用Semaphore或circom
    """
    proof_data = f"{wallet_address}:{risk_score}:{int(time.time())}"
    proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
    
    return {
        'proof_hash': proof_hash,
        'verified': True,
        'message': '风险分数已验证，钱包地址未泄露'
    }

@app.route('/api/verify_proof', methods=['POST'])
def verify_proof():
    data = request.json
    proof = generate_proof(data['wallet_hash'], data['risk_score'])
    return jsonify(proof)
```

2. **ESG绿色评分**
```python
# backend/services/sustainability.py
def calculate_sustainability(metrics):
    """
    基于Solana PoH能耗模型
    """
    # Solana平均能耗: 0.00051 kWh/tx
    energy_per_tx = 0.00051
    tx_count = metrics.get('volume_24h', 0) / 100  # 简化
    
    carbon_footprint = tx_count * energy_per_tx * 0.4  # kg CO2
    
    # 评分: 越低越好
    sustainable_score = max(0, 100 - int(carbon_footprint * 10))
    
    return sustainable_score
```

3. **社区反馈表单（Streamlit）**
```python
# feedback_app.py
import streamlit as st
import requests

st.title('🛡️ Prophet Sentinel 反馈系统')

protocol = st.text_input('协议名称')
actual_outcome = st.selectbox('实际结果', ['安全', '高风险', 'Rug Pull'])
predicted_score = st.slider('预测分数', 0, 100)

if st.button('提交反馈'):
    # 提交到GitHub Issue或数据库
    st.success('反馈已提交！您将获得10哨兵积分')
```

**输出：** 演示版高级功能

---

### 📅 **阶段8: 集成测试** (Day 8: 10/28, 6小时)

**目标：** 端到端测试和bug修复

#### 测试清单：

- [ ] **功能测试**
  - [ ] API响应正确性
  - [ ] 前端数据展示准确
  - [ ] Telegram Bot命令响应
  - [ ] 钱包连接流程

- [ ] **性能测试**
  - [ ] API响应时间 < 2秒
  - [ ] 前端加载时间 < 3秒
  - [ ] Bot推送延迟 < 2秒

- [ ] **边界测试**
  - [ ] 无效协议名处理
  - [ ] 网络错误处理
  - [ ] 并发请求处理

**输出：** 稳定的完整系统

---

### 📅 **阶段9: Demo准备** (Day 9: 10/29, 8小时)

**目标：** 录制演示视频和准备文档

#### 任务清单：

1. **录制Demo视频**（使用Loom/OBS）
   - [ ] 场景1: 打开Dashboard，展示风险热图（30秒）
   - [ ] 场景2: 使用Telegram Bot查询风险（30秒）
   - [ ] 场景3: 连接钱包，验证隐私分析（30秒）
   - [ ] 场景4: 展示ESG绿色评分（20秒）
   - [ ] 场景5: 触发高风险警报推送（20秒）
   - **总时长: 2-3分钟**

2. **撰写README**
```markdown
# 🧠 Prophet Sentinel

> AI预言 + 隐私盾 + 即时救赎，为DeFi用户提供链上风险防护

## 🎯 核心功能
- 实时风险预测（0-100分）
- Telegram即时警报
- 隐私保护分析
- 绿色可持续评分

## 🚀 快速开始
[安装步骤]

## 📊 技术架构
[架构图]

## 🎥 Demo视频
[Loom链接]
```

3. **Pitch材料**
   - [ ] 3分钟演讲稿
   - [ ] 核心亮点PPT（5页）
   - [ ] 数据支持（预测准确率、响应时间）

**输出：** 完整Demo材料包

---

### 📅 **阶段10: 部署上线** (Day 10: 10/30, 4小时)

**目标：** 云端部署并提交

#### 任务清单：

1. **后端部署（Render/Railway）**
```bash
# 部署Flask到Render
# 配置环境变量
# 测试API可访问性
```

2. **前端部署（Vercel/Netlify）**
```bash
npm run build
# 部署到Vercel
# 配置CORS
```

3. **最终检查**
   - [ ] 所有链接有效
   - [ ] Demo视频可播放
   - [ ] README完整
   - [ ] 代码注释清晰

**输出：** 上线的完整产品

---

## 🎯 关键成功因素

### MVP核心功能（必须完成）
1. ✅ ML风险预测模型（准确率>75%）
2. ✅ Flask API正常响应
3. ✅ React热图可视化
4. ✅ Telegram Bot基础命令

### 加分项（时间充裕时）
1. ⭐ zk隐私验证（哪怕是伪实现）
2. ⭐ ESG绿色评分
3. ⭐ 美观的UI设计
4. ⭐ 详细的技术文档

---

## ⚠️ 风险管理

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| ML模型训练不收敛 | 中 | 高 | 使用预训练模型或合成数据 |
| Solana API限流 | 高 | 中 | 添加缓存层和降级方案 |
| 前端开发延期 | 中 | 中 | 优先实现核心功能，UI简化 |
| 时间不足 | 高 | 高 | 严格按优先级，砍掉zk/社区模块 |

---

## 📈 每日检查点

每天结束前问自己：
- ✅ 今天的核心任务完成了吗？
- ✅ 代码能跑通吗？
- ✅ 有阻塞问题需要解决吗？
- ✅ 明天的任务清晰吗？

---

## 🎓 技术学习资源

### 快速参考
- **Solana开发**: https://docs.solana.com
- **Flask API**: https://flask.palletsprojects.com
- **Telegraf.js**: https://telegraf.js.org
- **Recharts**: https://recharts.org
- **zk-SNARK**: https://docs.circom.io (简化学习)

---

## 💡 最终建议

1. **第1-3天专注ML和后端** - 这是核心基础
2. **第4-6天完成前端和Bot** - 用户可见功能
3. **第7-8天集成和优化** - 确保稳定性
4. **第9-10天打磨和部署** - Demo质量决定成败

**记住：** 完成比完美更重要！先跑通MVP，再逐步优化。

---

**祝开发顺利！🚀**



