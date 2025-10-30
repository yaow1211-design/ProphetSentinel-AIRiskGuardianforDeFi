# Telegram Bot 网络连接问题解决方案

## ⚠️ 当前问题

Telegram Bot无法连接到 `api.telegram.org` 服务器。

**错误信息**: `ETIMEDOUT - 连接超时`

**原因**: 您的网络环境无法直接访问Telegram API服务器。

---

## 💡 解决方案

### 方案1: 使用VPN (推荐) ⭐

1. 连接到VPN服务
2. 重新启动Bot:
   ```bash
   cd telegram-bot
   npm start
   ```

### 方案2: 配置HTTP代理

1. 安装代理支持库:
   ```bash
   cd telegram-bot
   npm install https-proxy-agent
   ```

2. 编辑 `telegram-bot/.env` 文件，添加代理配置:
   ```bash
   # 添加以下两行
   TELEGRAM_PROXY_HOST=your-proxy-host
   TELEGRAM_PROXY_PORT=your-proxy-port
   ```

3. 重新启动Bot:
   ```bash
   npm start
   ```

### 方案3: 使用Web界面 (无需Telegram) ⭐

**直接访问前端Dashboard，功能完全可用！**

```bash
# 打开浏览器访问
http://localhost:3000
```

**功能包括**:
- 📊 实时风险监控面板
- 🔍 多协议风险分析
- 📈 风险热力图可视化
- 💹 绿色可持续性评分
- ⚡ 即时风险预测

---

## ✅ 当前可用服务

### 1. 后端API ✅ 运行中
- **地址**: http://localhost:5001
- **状态**: Healthy
- **功能**: 完全可用

**可用端点**:
```bash
# 健康检查
curl http://localhost:5001/api/health

# 风险预测
curl "http://localhost:5001/api/predict_risk?protocol=Jupiter"

# 协议列表
curl http://localhost:5001/api/protocols
```

### 2. 前端Dashboard ✅ 运行中
- **地址**: http://localhost:3000
- **状态**: 运行正常
- **功能**: 完全可用

### 3. Telegram Bot ⚠️ 等待网络连接
- **状态**: 代码已就绪
- **Token**: 已配置
- **问题**: 网络连接受限

---

## 🧪 测试网络连接

### 测试Telegram API可达性:
```bash
curl -v https://api.telegram.org
```

如果显示超时或连接失败，说明需要VPN或代理。

### 测试本地服务:
```bash
# 测试后端
curl http://localhost:5001/api/health

# 测试前端
curl http://localhost:3000
```

---

## 📝 Bot配置文件

当前配置文件: `telegram-bot/.env`

```bash
# 当前配置
TELEGRAM_BOT_TOKEN=8091713782:AAGfd2baFlirlVAwoG4Y_6_bI8jsDa4hXB0
BACKEND_API_URL=http://localhost:5001
DEVELOPMENT_MODE=true

# 如需代理，添加以下配置:
# TELEGRAM_PROXY_HOST=127.0.0.1
# TELEGRAM_PROXY_PORT=1087
```

---

## 🎯 推荐使用方式

**最佳方案**: 使用Web前端界面 (http://localhost:3000)

**优势**:
- ✅ 无需配置代理
- ✅ 功能完整
- ✅ 界面美观
- ✅ 实时更新
- ✅ 响应速度快

**Telegram Bot 优势**:
- 📱 移动端便捷
- 🔔 实时推送通知
- 💬 对话式交互
- ⏰ 定时风险监控

---

## 🔧 故障排查

### Bot无法启动
1. 检查Token是否正确
2. 测试网络连接
3. 查看日志: `cat logs/telegram-bot.log`

### 代理不工作
1. 确认代理服务器可用
2. 检查代理配置是否正确
3. 确保已安装 `https-proxy-agent`

### API调用失败
1. 确认后端服务运行中: `ps aux | grep "python app.py"`
2. 检查端口5001是否开放: `lsof -i :5001`
3. 测试API健康: `curl http://localhost:5001/api/health`

---

## 📞 支持

如有问题，请查看:
- 后端日志: `logs/backend.log`
- 前端日志: `logs/frontend.log`
- Bot日志: `logs/telegram-bot.log`

---

**更新时间**: 2025-10-30
**版本**: v1.0.0


