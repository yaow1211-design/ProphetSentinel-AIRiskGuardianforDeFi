#!/bin/bash
# Prophet Sentinel - 测试运行脚本

echo "🧪 Prophet Sentinel 测试套件"
echo "=============================="

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# 检查虚拟环境
if [ -d "backend/venv" ]; then
    echo "✅ 发现虚拟环境"
    source backend/venv/bin/activate
elif [ -d "venv" ]; then
    echo "✅ 发现虚拟环境"
    source venv/bin/activate
else
    echo "⚠️  未找到虚拟环境，使用系统Python"
    echo "建议: cd backend && python -m venv venv && source venv/bin/activate"
fi

# 检查pytest是否安装
if ! python -c "import pytest" 2>/dev/null; then
    echo "❌ pytest未安装"
    echo "安装中: pip install pytest pytest-cov"
    pip install pytest pytest-cov
fi

# 设置Python路径
export PYTHONPATH="${PROJECT_ROOT}:${PROJECT_ROOT}/backend:${PYTHONPATH}"

echo ""
echo "📦 Python路径: $PYTHONPATH"
echo "🐍 Python版本: $(python --version)"
echo ""

# 运行测试
echo "🚀 开始运行测试..."
echo ""

# 选项1: 运行所有测试
if [ "$1" == "all" ] || [ -z "$1" ]; then
    python -m pytest tests/ -v --tb=short
# 选项2: 运行指定测试文件
elif [ "$1" == "api" ]; then
    python -m pytest tests/test_api.py -v
elif [ "$1" == "model" ]; then
    python -m pytest tests/test_model.py -v
# 选项3: 运行指定测试并生成覆盖率报告
elif [ "$1" == "cov" ]; then
    python -m pytest tests/ --cov=backend --cov-report=html --cov-report=term
    echo ""
    echo "📊 覆盖率报告已生成: htmlcov/index.html"
# 选项4: 快速测试（只运行单元测试）
elif [ "$1" == "quick" ]; then
    python -m pytest tests/ -v --tb=line -x
else
    python -m pytest tests/ -v
fi

echo ""
echo "✨ 测试完成!"

