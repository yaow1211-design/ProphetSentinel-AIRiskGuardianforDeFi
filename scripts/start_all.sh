#!/bin/bash

# Prophet Sentinel - 一键启动脚本
# 用法: chmod +x scripts/start_all.sh && ./scripts/start_all.sh

set -e

echo "🚀 启动 Prophet Sentinel 完整系统..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 项目目录: $PROJECT_ROOT${NC}"
echo ""

# 检查环境
echo -e "${YELLOW}🔍 检查环境...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js 未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $(python3 --version)${NC}"
echo -e "${GREEN}✅ Node $(node --version)${NC}"
echo ""

# 检查.env文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env文件不存在，从模板复制...${NC}"
    cp .env.example .env
    echo -e "${RED}请编辑 .env 文件配置必要的环境变量！${NC}"
    exit 1
fi

# 1. 训练ML模型（如果不存在）
if [ ! -f backend/models/risk_model.pkl ]; then
    echo -e "${BLUE}🤖 训练ML模型...${NC}"
    cd backend
    
    if [ ! -d venv ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install -q -r requirements.txt
    python models/train_model.py
    deactivate
    cd ..
    echo ""
else
    echo -e "${GREEN}✅ ML模型已存在${NC}"
    echo ""
fi

# 2. 启动后端
echo -e "${BLUE}🔧 启动Flask后端...${NC}"
cd backend

if [ ! -d venv ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
else
    source venv/bin/activate
fi

# 后台运行Flask
python app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ 后端已启动 (PID: $BACKEND_PID)${NC}"
echo "   日志: logs/backend.log"
echo "   访问: http://localhost:5000"

deactivate
cd ..
echo ""

# 等待后端启动
echo -e "${YELLOW}⏳ 等待后端就绪...${NC}"
for i in {1..10}; do
    if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 后端API就绪${NC}"
        break
    fi
    sleep 1
done
echo ""

# 3. 启动前端
echo -e "${BLUE}🎨 启动React前端...${NC}"
cd frontend

if [ ! -d node_modules ]; then
    npm install
fi

# 后台运行React
BROWSER=none npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✅ 前端已启动 (PID: $FRONTEND_PID)${NC}"
echo "   日志: logs/frontend.log"
echo "   访问: http://localhost:3000"

cd ..
echo ""

# 4. 启动Telegram Bot（可选）
if [ ! -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo -e "${BLUE}🤖 启动Telegram Bot...${NC}"
    cd telegram-bot
    
    if [ ! -d node_modules ]; then
        npm install
    fi
    
    node bot.js > ../logs/telegram.log 2>&1 &
    BOT_PID=$!
    echo -e "${GREEN}✅ Telegram Bot已启动 (PID: $BOT_PID)${NC}"
    echo "   日志: logs/telegram.log"
    
    cd ..
    echo ""
else
    echo -e "${YELLOW}⚠️  跳过Telegram Bot（未配置TELEGRAM_BOT_TOKEN）${NC}"
    echo ""
fi

# 保存PID到文件
mkdir -p logs
echo "$BACKEND_PID" > logs/backend.pid
echo "$FRONTEND_PID" > logs/frontend.pid
if [ ! -z "$BOT_PID" ]; then
    echo "$BOT_PID" > logs/telegram.pid
fi

# 完成
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Prophet Sentinel 启动成功！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📡 访问地址：${NC}"
echo "   🌐 前端Dashboard: http://localhost:3000"
echo "   🔧 后端API:       http://localhost:5000"
echo "   📊 API文档:       http://localhost:5000/api"
echo ""
echo -e "${YELLOW}📝 日志文件：${NC}"
echo "   后端: logs/backend.log"
echo "   前端: logs/frontend.log"
if [ ! -z "$BOT_PID" ]; then
    echo "   Bot:  logs/telegram.log"
fi
echo ""
echo -e "${YELLOW}🛑 停止服务：${NC}"
echo "   运行: ./scripts/stop_all.sh"
echo "   或手动: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"


