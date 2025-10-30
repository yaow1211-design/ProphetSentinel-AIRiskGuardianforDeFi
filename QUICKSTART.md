# ⚡ Prophet Sentinel - 快速启动指南 | Quick Start Guide

**中文：** 目标：5分钟内启动完整系统  
**English:** Goal: Launch complete system in 5 minutes

---

## 🚀 一键启动（推荐）| One-Click Launch (Recommended)

### macOS/Linux

```bash
# 1. 克隆并进入项目 | Clone and enter project
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi

# 2. 配置环境变量 | Configure environment variables
cp .env.example .env
# 编辑 .env 填入你的 Telegram Bot Token | Edit .env and fill in your Telegram Bot Token

# 3. 训练ML模型 | Train ML model
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python models/train_model.py

# 4. 启动后端（新终端）| Start backend (new terminal)
python app.py

# 5. 启动前端（新终端）| Start frontend (new terminal)
cd ../frontend
npm install
npm start

# 6. 启动Telegram Bot（新终端，可选）| Start Telegram Bot (new terminal, optional)
cd ../telegram-bot
npm install
npm start
```

### Windows

```bash
# 1. 进入项目 | Enter project
cd C:\Users\YourName\Documents\ProphetSentinel-AIRiskGuardianforDeFi

# 2. 配置环境 | Configure environment
copy .env.example .env
# 编辑 .env | Edit .env

# 3. 训练模型 | Train model
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python models\train_model.py

# 4. 启动后端（新命令行）| Start backend (new command prompt)
python app.py

# 5. 启动前端（新命令行）| Start frontend (new command prompt)
cd ..\frontend
npm install
npm start

# 6. 启动Bot（可选）| Start Bot (optional)
cd ..\telegram-bot
npm install
npm start
```

---

## 📋 分步指南 | Step-by-Step Guide

### Step 1: 环境准备（2分钟）| Environment Setup (2 min)

```bash
# 检查Python版本 | Check Python version
python --version  # 需要 3.11+ | Requires 3.11+

# 检查Node版本 | Check Node version
node --version    # 需要 18+ | Requires 18+

# 检查npm | Check npm
npm --version
```

### Step 2: 训练ML模型（1分钟）| Train ML Model (1 min)

```bash
cd backend
python models/train_model.py
```

**预期输出 | Expected Output:**
```
🚀 Prophet Sentinel - 模型训练开始
🔧 生成 2000 条合成训练数据...
✅ 数据生成完成
🤖 开始训练模型...
🎯 模型训练完成! 准确率: 87.50%
💾 模型已保存: backend/models/risk_model.pkl
```

### Step 3: 启动后端（30秒）| Start Backend (30 sec)

```bash
# 在 backend/ 目录
python app.py
```

**测试API：**
```bash
# 新终端
curl "http://localhost:5000/api/health"
# 应返回: {"status": "healthy", ...}

curl "http://localhost:5000/api/predict_risk?protocol=Jupiter"
# 应返回风险数据JSON
```

### Step 4: 启动前端（1分钟）| Start Frontend (1 min)

```bash
cd frontend
npm install  # 首次需要 | First time only
npm start
```

**中文：** 访问 http://localhost:3000  
**English:** Visit http://localhost:3000

**预期效果 | Expected Results:**
- ✅ 看到渐变紫色背景 | See gradient purple background
- ✅ Hero标题 "🧠 Prophet Sentinel"
- ✅ 风险热图显示6个协议 | Risk heatmap shows 6 protocols
- ✅ 可以点击协议查看详情 | Click protocols to see details

### Step 5: 启动Telegram Bot（可选，30秒）| Start Telegram Bot (Optional, 30 sec)

```bash
# 先在 .env 设置 TELEGRAM_BOT_TOKEN | Set TELEGRAM_BOT_TOKEN in .env first
cd telegram-bot
npm install
npm start
```

**测试Bot | Test Bot:**
1. 在Telegram搜索你的Bot | Search for your Bot in Telegram
2. 发送 `/start` | Send `/start`
3. 发送 `/risk Jupiter` | Send `/risk Jupiter`

---

## 🎯 验证清单 | Verification Checklist

### 后端检查 | Backend Check
- [ ] http://localhost:5001 显示API文档 | Shows API docs
- [ ] http://localhost:5001/api/health 返回 | Returns `{"status": "healthy"}`
- [ ] http://localhost:5001/api/protocols 返回协议列表 | Returns protocol list
- [ ] http://localhost:5001/api/predict_risk?protocol=Jupiter 返回风险数据 | Returns risk data

### 前端检查 | Frontend Check
- [ ] http://localhost:3000 正常加载 | Loads normally
- [ ] 风险热图显示6个协议柱状图 | Heatmap shows 6 protocol bars
- [ ] 柱状图颜色正确（绿/黄/红）| Bar colors correct (green/yellow/red)
- [ ] 点击协议后显示详情卡片 | Click protocol shows detail card
- [ ] 30秒后数据自动刷新 | Data auto-refreshes after 30s

### Bot检查（如果启动）| Bot Check (If Started)
- [ ] Bot在线 | Bot is online
- [ ] `/start` 返回欢迎消息 | Returns welcome message
- [ ] `/risk Jupiter` 返回风险分析 | Returns risk analysis
- [ ] `/protocols` 显示协议列表 | Shows protocol list

---

## 🐛 常见问题 | Common Issues

### Q1: 后端启动失败 "ModuleNotFoundError"
```bash
# 确保已激活虚拟环境
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 重新安装依赖
pip install -r requirements.txt
```

### Q2: 前端无法连接后端
```bash
# 检查后端是否运行
curl http://localhost:5000/api/health

# 检查CORS配置
# 确保 backend/app.py 中有 CORS(app)
```

### Q3: 模型文件不存在
```bash
# 重新训练模型
cd backend
python models/train_model.py

# 检查文件是否生成
ls -la models/risk_model.pkl
```

### Q4: Telegram Bot无响应
```bash
# 检查token是否正确
echo $TELEGRAM_BOT_TOKEN

# 查看Bot日志
# 应显示 "✅ Bot已启动! 等待消息..."
```

### Q5: npm install 很慢
```bash
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install
```

---

## 📊 性能优化 | Performance Optimization

### 后端优化 | Backend Optimization
```bash
# 使用生产服务器
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 前端优化
```bash
# 构建生产版本
npm run build

# 使用serve托管
npx serve -s build
```

---

## 🔧 开发模式

### 热重载开发

**后端：**
```bash
pip install flask[async]
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

**前端：**
```bash
npm start  # 自动热重载
```

**Bot：**
```bash
npm install -D nodemon
npm run dev  # 使用nodemon
```

---

## 📦 Docker部署（高级）

```bash
# 待添加 Dockerfile
docker-compose up -d
```

---

## 🎉 成功！

如果以上步骤都完成，你应该看到：

1. ✅ **后端API** 在 http://localhost:5000 运行
2. ✅ **前端Dashboard** 在 http://localhost:3000 显示
3. ✅ **Telegram Bot** 可以响应命令
4. ✅ **风险热图** 实时更新数据

**下一步：**
- 📖 阅读 [README.md](README.md) 了解详细功能
- 🛠️ 查看 [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) 学习开发流程
- 📚 访问 [TECH_STACK.md](TECH_STACK.md) 了解技术栈

---

**需要帮助？** 
- GitHub Issues: https://github.com/yourusername/prophet-sentinel/issues
- Telegram: @ProphetSentinelSupport
- Email: support@prophetsentinel.com

**祝你使用愉快！🚀**




