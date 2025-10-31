#!/bin/bash

# 设置工作目录
cd "$(dirname "$0")"
PROJECT_ROOT=$(cd .. && pwd)

# 加载环境变量
source "$PROJECT_ROOT/config/prod/backend.env"
source "$PROJECT_ROOT/config/prod/telegram.env"

echo "启动 Prophet Sentinel 服务..."

# 启动后端服务
echo "启动后端服务..."
cd "$PROJECT_ROOT/backend"
python3 app.py &
BACKEND_PID=$!

# 启动前端服务
echo "启动前端服务..."
cd "$PROJECT_ROOT/frontend"
npm run build
npx serve -s build &
FRONTEND_PID=$!

# 启动 Telegram Bot
echo "启动 Telegram Bot..."
cd "$PROJECT_ROOT/telegram-bot"
node bot.js &
BOT_PID=$!

# 保存进程 ID
echo $BACKEND_PID > /tmp/prophet-sentinel-backend.pid
echo $FRONTEND_PID > /tmp/prophet-sentinel-frontend.pid
echo $BOT_PID > /tmp/prophet-sentinel-bot.pid

echo "所有服务已启动。"
echo "后端 PID: $BACKEND_PID"
echo "前端 PID: $FRONTEND_PID"
echo "Bot PID: $BOT_PID"