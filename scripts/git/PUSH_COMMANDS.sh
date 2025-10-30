#!/bin/bash
# Prophet Sentinel - GitHub 推送脚本
# 执行前请先添加 SSH 公钥到 GitHub: https://github.com/settings/keys

echo "=================================="
echo "🚀 Prophet Sentinel 推送到 GitHub"
echo "=================================="
echo ""

# 进入项目目录
cd /Users/tutu/Documents/ProphetSentinel-AIRiskGuardianforDeFi

echo "📁 当前目录: $(pwd)"
echo ""

# 显示待推送的提交
echo "📝 待推送的提交:"
git log --oneline origin/main..HEAD 2>/dev/null || git log --oneline -5
echo ""

# 切换到 SSH URL
echo "🔧 配置 SSH remote..."
git remote set-url origin git@github.com:yaow1211-design/ProphetSentinel-AIRiskGuardianforDeFi.git
echo "✅ Remote URL 已切换为 SSH"
echo ""

# 测试 SSH 连接
echo "🔐 测试 GitHub SSH 连接..."
ssh -T git@github.com 2>&1 | head -3
echo ""

# 提示用户
echo "⚠️  如果上面显示 'Permission denied'，请先添加 SSH 公钥到 GitHub："
echo "   1. 访问: https://github.com/settings/keys"
echo "   2. 点击 'New SSH key'"
echo "   3. 复制粘贴这个公钥:"
echo ""
cat ~/.ssh/id_ed25519.pub
echo ""
echo "   4. 点击 'Add SSH key'"
echo ""
read -p "已添加 SSH 公钥？按回车继续推送... " 

# 推送
echo ""
echo "🚀 开始推送到 GitHub..."
git push origin main

# 检查结果
if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✅ 推送成功！"
    echo "=================================="
    echo ""
    echo "🌐 访问你的仓库:"
    echo "   https://github.com/yaow1211-design/ProphetSentinel-AIRiskGuardianforDeFi"
    echo ""
    echo "📊 推送内容:"
    echo "   - 5 个提交"
    echo "   - 57 个文件"
    echo "   - ~730 KB"
    echo ""
else
    echo ""
    echo "=================================="
    echo "❌ 推送失败"
    echo "=================================="
    echo ""
    echo "💡 请查看错误信息，或参考文档:"
    echo "   - QUICK_SSH_SETUP.md"
    echo "   - NETWORK_TROUBLESHOOTING.md"
    echo ""
fi

