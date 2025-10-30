# 🚀 启动 Prophet Sentinel 服务

> 快速启动后端 API 和前端 Dashboard

---

## 📋 启动顺序

### 1️⃣ **启动后端 API** (Flask - 端口 5000)

```bash
# 进入后端目录
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi/backend

# 激活虚拟环境（如果有）
source venv/bin/activate  # 或者你的虚拟环境路径

# 安装依赖（首次运行）
pip install -r requirements.txt

# 启动后端
python app.py
```

**应该看到**:
```
🚀 启动 Prophet Sentinel API...
✅ 服务初始化成功
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://172.20.10.2:5000
```

---

### 2️⃣ **启动前端 Dashboard** (React - 端口 3000)

**打开新的终端窗口**，然后执行：

```bash
# 进入前端目录
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi/frontend

# 安装依赖（首次运行）
npm install

# 启动前端
npm start
```

**应该看到**:
```
Compiled successfully!

You can now view prophet-sentinel-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://172.20.10.2:3000
```

浏览器会自动打开 http://localhost:3000

---

### 3️⃣ **启动 Telegram Bot** (可选)

**打开第三个终端窗口**：

```bash
# 进入 Bot 目录
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi/telegram-bot

# 安装依赖（首次运行）
npm install

# 启动 Bot（需要配置 TELEGRAM_BOT_TOKEN）
npm start
```

---

## ⚡ **一键启动脚本**

使用项目自带的启动脚本：

```bash
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi
chmod +x scripts/start_all.sh
./scripts/start_all.sh
```

---

## 🔗 **访问地址**

启动成功后访问：

| 服务 | 地址 | 说明 |
|------|------|------|
| 🌐 **前端 Dashboard** | http://localhost:3000 | React 风险监控面板 |
| 🔌 **后端 API** | http://localhost:5000 | Flask REST API |
| 📊 **API 文档** | http://localhost:5000/api/health | 健康检查 |
| 🧪 **风险预测** | http://localhost:5000/api/predict_risk?protocol=Jupiter | 测试 API |

---

## 🛠️ **常见问题**

### Q: 后端启动失败 "ModuleNotFoundError"
**解决**:
```bash
cd backend
pip install -r requirements.txt
```

### Q: 前端启动失败 "npm ERR!"
**解决**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Q: 端口被占用
**解决**:
- 后端：修改 `backend/config.py` 中的 `PORT`
- 前端：设置环境变量 `PORT=3001 npm start`

### Q: API 连接失败
**检查**:
1. 后端是否在 5000 端口运行
2. 前端 `src/services/api.js` 中的 API 地址是否正确

---

## 📝 **开发模式启动命令**

### 终端 1 - 后端
```bash
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi/backend
python app.py
```

### 终端 2 - 前端  
```bash
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi/frontend
npm start
```

### 终端 3 - Bot (可选)
```bash
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi/telegram-bot
npm start
```

---

## 🎯 **验证启动成功**

1. **后端验证**:
   ```bash
   curl http://localhost:5000/api/health
   ```
   
2. **前端验证**:
   访问 http://localhost:3000 看到 Prophet Sentinel 界面
   
3. **API 测试**:
   ```bash
   curl "http://localhost:5000/api/predict_risk?protocol=Jupiter"
   ```

---

**创建时间**: 2025-10-27  
**适用版本**: Prophet Sentinel v1.0
