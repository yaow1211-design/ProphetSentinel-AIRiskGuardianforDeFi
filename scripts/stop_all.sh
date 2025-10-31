#!/bin/bash

# Prophet Sentinel - 停止所有服务
# 用法: ./scripts/stop_all.sh

echo "🛑 停止 Prophet Sentinel 服务..."
echo ""

# 从PID文件读取并终止进程
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        echo "✅ 后端已停止 (PID: $BACKEND_PID)"
    fi
    rm logs/backend.pid
fi

if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID
        echo "✅ 前端已停止 (PID: $FRONTEND_PID)"
    fi
    rm logs/frontend.pid
fi

if [ -f logs/telegram.pid ]; then
    BOT_PID=$(cat logs/telegram.pid)
    if ps -p $BOT_PID > /dev/null 2>&1; then
        kill $BOT_PID
        echo "✅ Telegram Bot已停止 (PID: $BOT_PID)"
    fi
    rm logs/telegram.pid
fi

# 清理可能的僵尸进程
pkill -f "python app.py" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null
pkill -f "node bot.js" 2>/dev/null

echo ""
echo "🎉 所有服务已停止"








