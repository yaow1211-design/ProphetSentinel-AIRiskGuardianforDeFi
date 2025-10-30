# 📖 Prophet Sentinel - 使用指南

**版本：** v1.0  
**更新时间：** 2025-10-23

---

## 目录

1. [系统要求](#系统要求)
2. [安装步骤](#安装步骤)
3. [基础使用](#基础使用)
4. [高级功能](#高级功能)
5. [API参考](#api参考)
6. [故障排除](#故障排除)
7. [最佳实践](#最佳实践)

---

## 系统要求

### 最低配置
- **操作系统:** macOS 10.15+ / Ubuntu 20.04+ / Windows 10+
- **Python:** 3.11或更高
- **Node.js:** 18.0或更高
- **内存:** 4GB RAM
- **磁盘:** 2GB可用空间

### 推荐配置
- **内存:** 8GB RAM
- **CPU:** 4核
- **网络:** 稳定的互联网连接（访问Solana RPC）

---

## 安装步骤

### 方法1: 自动安装（推荐）

```bash
# 1. 进入项目目录
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi

# 2. 运行一键启动脚本
./scripts/start_all.sh
```

### 方法2: 手动安装

#### Step 1: 后端设置

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 训练ML模型
python models/train_model.py
```

#### Step 2: 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 或使用yarn
yarn install
```

#### Step 3: Bot设置（可选）

```bash
cd telegram-bot

# 安装依赖
npm install
```

---

## 基础使用

### 启动系统

#### 启动后端

```bash
cd backend
source venv/bin/activate
python app.py
```

**成功标志：**
```
🚀 启动 Prophet Sentinel API...
✅ 服务初始化成功
 * Running on http://0.0.0.0:5000
```

#### 启动前端

```bash
cd frontend
npm start
```

**成功标志：**
- 浏览器自动打开 http://localhost:3000
- 显示紫色渐变背景和风险热图

#### 启动Telegram Bot

```bash
cd telegram-bot
npm start
```

**成功标志：**
```
🚀 启动 Prophet Sentinel Bot...
✅ Bot已启动! 等待消息...
```

---

## 核心功能使用

### 1. 查看风险热图

**操作步骤：**
1. 访问 http://localhost:3000
2. 查看6个协议的柱状图
3. 颜色说明：
   - 🟢 绿色 (0-30): 低风险
   - 🟡 黄色 (30-70): 中风险
   - 🔴 红色 (70-100): 高风险

**交互功能：**
- 点击任意协议柱查看详情
- 点击"刷新"按钮手动更新
- 系统每30秒自动刷新

### 2. 查看协议详情

**操作步骤：**
1. 在热图中点击协议名
2. 查看详细信息：
   - 风险分数 (0-100)
   - 绿色评分 (0-100)
   - 24h交易量
   - 流动性变化
   - 鲸鱼转移次数
   - 持有集中度

**解读指南：**
- **风险分数 > 70:** 立即检查持仓
- **流动性变化 < -20%:** 警惕流动性危机
- **鲸鱼转移 > 10次:** 异常活动
- **持有集中度 > 80%:** 高度中心化风险

### 3. 使用Telegram Bot

**基础命令：**

```
/start
→ 显示欢迎消息和命令列表

/risk Jupiter
→ 查询Jupiter的实时风险

/protocols
→ 显示所有支持的协议

/subscribe
→ 订阅高风险警报

/unsubscribe
→ 取消订阅
```

**高级用法：**

```bash
# 批量查询
/risk Orca
/risk Raydium
/risk Serum

# 订阅后自动接收警报
# 当任意协议风险分数 > 80 时
# Bot会自动推送消息
```

### 4. 调用API

**使用curl：**

```bash
# 健康检查
curl http://localhost:5000/api/health

# 查询风险
curl "http://localhost:5000/api/predict_risk?protocol=Jupiter"

# 获取协议列表
curl http://localhost:5000/api/protocols

# zk验证
curl -X POST http://localhost:5000/api/verify_proof \
  -H "Content-Type: application/json" \
  -d '{"wallet_hash": "abc123", "risk_score": 75}'
```

**使用Python：**

```python
import requests

# 查询风险
response = requests.get(
    'http://localhost:5000/api/predict_risk',
    params={'protocol': 'Jupiter'}
)

data = response.json()
print(f"风险分数: {data['risk_score']}")
print(f"绿色评分: {data['sustainable_score']}")
```

**使用JavaScript：**

```javascript
// 查询风险
fetch('http://localhost:5000/api/predict_risk?protocol=Jupiter')
  .then(res => res.json())
  .then(data => {
    console.log('风险分数:', data.risk_score);
    console.log('警报等级:', data.alert_level);
  });
```

---

## 高级功能

### 自定义风险阈值

编辑 `backend/config.py`：

```python
# 风险阈值
RISK_THRESHOLD_LOW = 30    # 低风险上限
RISK_THRESHOLD_MEDIUM = 70  # 中风险上限
RISK_THRESHOLD_HIGH = 90    # 高风险上限
```

### 调整ML模型参数

编辑 `backend/models/train_model.py`：

```python
model = RandomForestClassifier(
    n_estimators=200,    # 树的数量（默认100）
    max_depth=15,        # 最大深度（默认10）
    min_samples_split=3, # 最小分裂样本（默认5）
    random_state=42
)
```

### 添加新协议

#### 1. 后端添加数据

编辑 `backend/services/solana_service.py`：

```python
PROTOCOL_DATA = {
    # ... 现有协议
    'NewProtocol': {
        'volume_base': 10000000,
        'liquidity_base': 50000000,
        'risk_base': 40
    }
}
```

#### 2. 前端添加显示

编辑 `frontend/src/components/RiskHeatmap.js`：

```javascript
const PROTOCOLS = [
  'Jupiter', 'Orca', 'Raydium', 
  'Serum', 'Marinade', 'Solend',
  'NewProtocol'  // 添加新协议
];
```

### 配置真实Solana RPC

编辑 `.env` 文件：

```bash
# 使用Helius API（推荐）
HELIUS_API_KEY=your-helius-api-key
SOLANA_RPC_URL=https://mainnet.helius-rpc.com/?api-key=${HELIUS_API_KEY}

# 或使用QuickNode
SOLANA_RPC_URL=https://your-endpoint.solana-mainnet.quiknode.pro/xxx/
```

---

## API参考

### GET /api/predict_risk

**描述:** 获取协议风险预测

**参数:**
- `protocol` (string, required): 协议名称

**响应:**
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

### GET /api/protocols

**描述:** 获取支持的协议列表

**响应:**
```json
{
  "protocols": [
    {
      "name": "Jupiter",
      "type": "DEX Aggregator",
      "supported": true
    }
  ],
  "total": 6
}
```

### GET /api/health

**描述:** 系统健康检查

**响应:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T12:00:00Z",
  "model_loaded": true,
  "solana_connected": true
}
```

### POST /api/verify_proof

**描述:** zk隐私验证

**请求体:**
```json
{
  "wallet_hash": "abc123...",
  "risk_score": 75
}
```

**响应:**
```json
{
  "verified": true,
  "proof_hash": "def456...",
  "message": "✅ 风险分数已验证，钱包地址未泄露",
  "timestamp": "2025-10-23T12:00:00Z"
}
```

---

## 故障排除

### 问题1: 后端启动失败

**错误信息:**
```
ModuleNotFoundError: No module named 'flask'
```

**解决方案:**
```bash
# 确保已激活虚拟环境
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

### 问题2: 前端无法连接后端

**错误信息:**
```
Network Error: Failed to fetch
```

**解决方案:**
```bash
# 1. 检查后端是否运行
curl http://localhost:5000/api/health

# 2. 检查CORS配置
# 确保 backend/app.py 中有：
CORS(app)

# 3. 检查防火墙
# macOS: 系统偏好设置 -> 安全性与隐私 -> 防火墙
```

### 问题3: 模型预测不准确

**可能原因:**
- 训练数据不足
- 模型参数需要调整

**解决方案:**
```bash
# 重新训练模型（更多样本）
cd backend
python models/train_model.py

# 编辑训练脚本增加样本数
# 将 n_samples=2000 改为 n_samples=5000
```

### 问题4: Telegram Bot无响应

**检查清单:**
```bash
# 1. 检查Token是否正确
echo $TELEGRAM_BOT_TOKEN

# 2. 检查Bot是否运行
ps aux | grep "node bot.js"

# 3. 查看日志
tail -f logs/telegram.log

# 4. 测试API连接
curl http://localhost:5000/api/health
```

### 问题5: 端口被占用

**错误信息:**
```
Error: listen EADDRINUSE: address already in use :::5000
```

**解决方案:**
```bash
# 查找占用端口的进程
lsof -i :5000

# 终止进程
kill -9 <PID>

# 或使用其他端口
# 编辑 .env
FLASK_PORT=5001
```

---

## 最佳实践

### 性能优化

1. **使用生产服务器**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **启用前端生产构建**
```bash
npm run build
npx serve -s build
```

3. **配置缓存**
```bash
# 安装Redis
pip install redis

# 启用缓存（编辑 backend/app.py）
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 安全建议

1. **修改默认密钥**
```bash
# 编辑 .env
FLASK_SECRET_KEY=$(openssl rand -hex 32)
```

2. **限制API访问**
```python
# 添加到 backend/app.py
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per minute"])
```

3. **使用HTTPS**
```bash
# 生产环境部署时启用SSL
```

### 监控与日志

1. **查看实时日志**
```bash
# 后端
tail -f logs/backend.log

# 前端
tail -f logs/frontend.log

# Bot
tail -f logs/telegram.log
```

2. **日志级别配置**
```python
# 编辑 backend/utils/logger.py
logger.setLevel(logging.DEBUG)  # 详细日志
logger.setLevel(logging.INFO)   # 标准日志
logger.setLevel(logging.WARNING) # 仅警告
```

---

## 常见使用场景

### 场景1: 定期风险检查

```bash
# 每天早上10点检查所有协议
crontab -e

# 添加：
0 10 * * * cd /path/to/project && python scripts/daily_check.py
```

### 场景2: 集成到现有系统

```python
# 在你的Python应用中
import requests

def check_protocol_risk(protocol):
    url = 'http://localhost:5000/api/predict_risk'
    response = requests.get(url, params={'protocol': protocol})
    data = response.json()
    
    if data['risk_score'] > 70:
        send_alert(f"⚠️ {protocol} 高风险!")
    
    return data
```

### 场景3: 批量分析

```python
protocols = ['Jupiter', 'Orca', 'Raydium']
results = []

for protocol in protocols:
    data = check_protocol_risk(protocol)
    results.append(data)

# 生成报告
generate_risk_report(results)
```

---

## 升级与维护

### 更新依赖

```bash
# Python
pip install --upgrade -r requirements.txt

# Node.js
npm update
```

### 备份数据

```bash
# 备份训练好的模型
cp backend/models/risk_model.pkl backup/

# 备份配置
cp .env backup/
```

### 版本管理

```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

---

## 获取帮助

### 文档资源
- [README.md](README.md) - 项目概述
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) - 开发指南
- [TECH_STACK.md](TECH_STACK.md) - 技术栈详解

### 社区支持
- **GitHub Issues:** https://github.com/yourusername/prophet-sentinel/issues
- **Telegram群:** @ProphetSentinelSupport
- **Email:** support@prophetsentinel.com

### 贡献代码
- Fork仓库
- 创建功能分支
- 提交Pull Request

---

**祝你使用愉快！如有问题，随时联系我们。🚀**




