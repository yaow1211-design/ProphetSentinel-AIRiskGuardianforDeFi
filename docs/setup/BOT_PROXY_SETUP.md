# Telegram Bot 代理配置指南 | Proxy Setup Guide

## 📋 已完成的配置 | Completed Configuration

### ✅ 1. 代理代码修复
- 文件: `telegram-bot/bot.js`
- 修复: `HttpsProxyAgent` 引入方式
- 状态: ✅ 完成

### ✅ 2. 安装代理依赖
```bash
npm install https-proxy-agent
```
状态: ✅ 已安装

### ✅ 3. .env 配置
文件位置: `telegram-bot/.env`

```bash
TELEGRAM_PROXY_HOST=127.0.0.1
TELEGRAM_PROXY_PORT=7890
```

---

## 🔧 配置步骤 | Configuration Steps

### 第一步：确认代理软件运行

**常见代理软件及默认端口:**

| 软件 | 默认端口 | 检查方法 |
|------|---------|---------|
| Clash | 7890 | 系统托盘查看图标 |
| ClashX | 7890 | 菜单栏查看状态 |
| V2Ray | 10809 | 检查配置文件 |
| Shadowsocks | 1080 | 系统托盘确认 |

### 第二步：查找实际端口

**macOS Clash查看方法:**
1. 点击菜单栏Clash图标
2. 选择"配置" → "设置"
3. 查看"混合代理端口"或"HTTP端口"

**测试代理连接:**
```bash
# 替换7890为你的实际端口
curl -x http://127.0.0.1:7890 https://api.telegram.org
```

如果成功返回数据，说明代理可用。

### 第三步：修改.env配置

编辑 `telegram-bot/.env` 文件，修改端口为实际端口：

```bash
# 示例1: Clash
TELEGRAM_PROXY_HOST=127.0.0.1
TELEGRAM_PROXY_PORT=7890

# 示例2: V2Ray
TELEGRAM_PROXY_HOST=127.0.0.1
TELEGRAM_PROXY_PORT=10809

# 示例3: 自定义
TELEGRAM_PROXY_HOST=127.0.0.1
TELEGRAM_PROXY_PORT=你的端口
```

### 第四步：重启Bot

```bash
# 停止旧进程
pkill -f "node bot.js"

# 启动Bot
cd telegram-bot
npm start
```

---

## 🧪 验证配置 | Verify Configuration

### 1. 检查Bot日志
```bash
tail -f logs/telegram-bot.log
```

**成功标志:**
```
🔧 使用代理: http://127.0.0.1:7890
🚀 启动 Prophet Sentinel Bot...
📡 API地址: http://localhost:5001
✅ Bot已启动! 等待消息...
```

**失败标志:**
```
❌ Bot启动失败: ETIMEDOUT
```

### 2. 测试Bot响应
在Telegram中:
1. 搜索你的Bot
2. 发送 `/start`
3. 应该收到欢迎消息

---

## 🐛 故障排查 | Troubleshooting

### 问题1: 仍然显示ETIMEDOUT

**原因:** 代理未运行或端口不正确

**解决:**
1. 确认代理软件正在运行
2. 检查端口号是否正确
3. 测试代理: `curl -x http://127.0.0.1:7890 https://google.com`

### 问题2: TypeError: HttpsProxyAgent is not a constructor

**原因:** 依赖未安装或版本问题

**解决:**
```bash
cd telegram-bot
npm install https-proxy-agent
```

### 问题3: 代理连接被拒绝

**原因:** 端口错误或代理未开启HTTP代理

**解决:**
1. 检查代理设置中是否开启HTTP代理
2. 尝试其他端口

---

## 💡 替代方案 | Alternative Solutions

### 方案1: 使用VPN (最简单)
1. 开启VPN
2. 不需要配置代理，直接启动Bot
3. Bot会直接连接Telegram

### 方案2: 使用系统代理
某些代理软件支持系统级代理，Bot可能自动使用。

### 方案3: 使用Web界面 (推荐)
如果代理配置复杂，建议使用Web界面:
- 访问: http://localhost:3000
- 功能完全相同
- 无需处理网络问题

---

## 📞 当前配置状态

```
✅ 代理代码: 已修复
✅ 代理依赖: 已安装
✅ 代理配置: 已添加
✅ Bot进程: 运行中
⏳ 连接状态: 等待代理生效
```

**下一步:** 确保您的代理软件(Clash/V2Ray等)正在运行，并且端口号正确。

---

**生成时间:** 2025-10-30  
**版本:** v1.0
