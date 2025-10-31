# 🤖 Telegram Bot 环境配置

## 🔧 配置步骤

### 1. 创建 .env 文件

在 `telegram-bot/` 目录下创建 `.env` 文件：

```bash
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi/telegram-bot
touch .env
```

### 2. 填入配置内容

将以下内容复制到 `.env` 文件：

```env
# Telegram Bot Token - 从 @BotFather 获取
TELEGRAM_BOT_TOKEN=your_bot_token_here

# 后端 API 地址
BACKEND_API_URL=http://localhost:5000

# 管理员聊天 ID（可选）
ADMIN_CHAT_ID=

# 日志级别
LOG_LEVEL=info

# 是否启用开发模式
DEVELOPMENT_MODE=true
```

### 3. 获取 Telegram Bot Token

1. 在 Telegram 中找到 @BotFather
2. 发送 `/newbot` 命令
3. 按提示设置 bot 名称和用户名
4. 复制获得的 token 到 `.env` 文件

### 4. 启动 Bot

```bash
npm start
```

## 🎯 快速演示（跳过 Token）

如果暂时不想配置 Telegram，可以注释掉 bot 启动代码，让其在演示模式运行。

## 🔍 常见问题

### Q: 找不到 @BotFather
**A**: 在 Telegram 搜索框输入 `@BotFather`

### Q: Token 格式错误
**A**: Token 格式应该是 `123456789:ABCDEF...`

### Q: Bot 无响应
**A**: 检查 token 是否正确，网络是否正常





