/**
 * Prophet Sentinel - Telegram警报Bot
 * 提供实时风险查询和高风险推送功能
 */

const { Telegraf } = require('telegraf');
const axios = require('axios');
require('dotenv').config();

// 配置
const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const API_BASE = process.env.BACKEND_API_URL || 'http://localhost:5001';

if (!BOT_TOKEN) {
    console.error('❌ 错误: 请在.env文件中设置 TELEGRAM_BOT_TOKEN');
    process.exit(1);
}

// 创建Bot实例
const botOptions = {
    handlerTimeout: 900000, // 15分钟超时
};

// 如果配置了代理，使用代理
if (process.env.TELEGRAM_PROXY_HOST && process.env.TELEGRAM_PROXY_PORT) {
    const { HttpsProxyAgent } = require('https-proxy-agent');
    const proxyUrl = `http://${process.env.TELEGRAM_PROXY_HOST}:${process.env.TELEGRAM_PROXY_PORT}`;
    botOptions.telegram = {
        agent: new HttpsProxyAgent(proxyUrl)
    };
    console.log(`🔧 使用代理: ${proxyUrl}`);
}

const bot = new Telegraf(BOT_TOKEN, botOptions);

// 订阅用户存储（生产环境应使用数据库）
const subscribers = new Set();

// ==================== 命令处理 ====================

// /start 命令
bot.start((ctx) => {
    const welcomeMessage = `
🧠 *欢迎使用 Prophet Sentinel!*

我是您的DeFi风险哨兵，提供实时链上风险预测。

📌 *可用命令:*
/risk <协议名> - 查询协议风险
/protocols - 查看支持的协议列表
/subscribe - 订阅高风险警报
/unsubscribe - 取消订阅
/help - 查看帮助信息

💡 *示例:*
/risk Jupiter
/risk Orca

让我们开始守护您的DeFi资产! 🛡️
    `;
    
    ctx.replyWithMarkdown(welcomeMessage);
});

// /help 命令
bot.help((ctx) => {
    const helpMessage = `
🔧 *命令帮助*

*风险查询:*
/risk <协议名> - 查询指定协议的风险分数
例: /risk Jupiter

*协议列表:*
/protocols - 显示所有支持的DeFi协议

*警报订阅:*
/subscribe - 订阅高风险警报（风险分数>70自动推送）
/unsubscribe - 取消订阅

*其他:*
/help - 显示此帮助信息
/about - 关于Prophet Sentinel

⚡ *风险等级:*
🟢 0-30: 低风险
🟡 30-70: 中风险  
🔴 70-100: 高风险
    `;
    
    ctx.replyWithMarkdown(helpMessage);
});

// /risk 命令 - 查询风险
bot.command('risk', async (ctx) => {
    try {
        // 提取协议名
        const args = ctx.message.text.split(' ');
        const protocol = args[1] || 'Jupiter';
        
        // 发送"正在查询"提示
        const loadingMsg = await ctx.reply(`🔍 正在查询 ${protocol} 的风险数据...`);
        
        // 调用API
        const response = await axios.get(`${API_BASE}/api/predict_risk`, {
            params: { protocol },
            timeout: 5000
        });
        
        const data = response.data;
        
        // 删除加载提示
        await ctx.deleteMessage(loadingMsg.message_id);
        
        // 构建响应消息
        const riskMessage = formatRiskMessage(data);
        
        await ctx.replyWithMarkdown(riskMessage);
        
    } catch (error) {
        console.error('查询风险失败:', error.message);
        
        ctx.reply(
            '❌ 查询失败，请稍后重试。\n\n' +
            '可能原因:\n' +
            '• 后端服务未启动\n' +
            '• 协议名称错误\n' +
            '• 网络连接问题'
        );
    }
});

// /protocols 命令 - 协议列表
bot.command('protocols', async (ctx) => {
    try {
        const response = await axios.get(`${API_BASE}/api/protocols`);
        const protocols = response.data.protocols;
        
        let message = '📋 *支持的DeFi协议:*\n\n';
        
        protocols.forEach((p, index) => {
            const status = p.supported ? '✅' : '🔜';
            message += `${index + 1}. ${status} *${p.name}* - ${p.type}\n`;
        });
        
        message += '\n使用 /risk <协议名> 查询风险';
        
        ctx.replyWithMarkdown(message);
        
    } catch (error) {
        ctx.reply('❌ 获取协议列表失败');
    }
});

// /subscribe 命令 - 订阅警报
bot.command('subscribe', (ctx) => {
    const chatId = ctx.chat.id;
    
    if (subscribers.has(chatId)) {
        ctx.reply('⚠️ 您已经订阅了高风险警报');
    } else {
        subscribers.add(chatId);
        
        ctx.replyWithMarkdown(`
✅ *订阅成功!*

当检测到以下情况时，我会立即通知您:
• 风险分数 > 70 的协议
• 流动性骤降 > 30%
• 鲸鱼异常活动

您可以随时使用 /unsubscribe 取消订阅
        `);
        
        console.log(`➕ 新订阅: ${chatId}`);
    }
});

// /unsubscribe 命令 - 取消订阅
bot.command('unsubscribe', (ctx) => {
    const chatId = ctx.chat.id;
    
    if (subscribers.has(chatId)) {
        subscribers.delete(chatId);
        ctx.reply('✅ 已取消订阅警报');
        console.log(`➖ 取消订阅: ${chatId}`);
    } else {
        ctx.reply('⚠️ 您还未订阅警报');
    }
});

// /about 命令
bot.command('about', (ctx) => {
    ctx.replyWithMarkdown(`
🧠 *Prophet Sentinel*

AI驱动的DeFi风险预测系统

*核心功能:*
• 🎯 实时风险预测 (0-100分)
• 🌱 ESG绿色评分
• 🔒 隐私保护分析
• ⚡ 即时警报推送

*技术栈:*
• Python + scikit-learn (ML)
• Flask (后端API)
• Solana Web3.js (链上数据)
• Telegraf.js (Bot框架)

GitHub: [待添加]
版本: v1.0.0
    `);
});

// ==================== 辅助函数 ====================

/**
 * 格式化风险消息
 */
function formatRiskMessage(data) {
    const { protocol, risk_score, alert_emoji, alert_level, sustainable_score, metrics, timestamp } = data;
    
    // 风险等级描述
    let riskDesc;
    if (risk_score < 30) {
        riskDesc = '低风险，相对安全';
    } else if (risk_score < 70) {
        riskDesc = '中等风险，谨慎使用';
    } else if (risk_score < 90) {
        riskDesc = '高风险，建议撤离';
    } else {
        riskDesc = '极高风险，立即撤离!';
    }
    
    // 可持续性描述
    let esgDesc;
    if (sustainable_score >= 85) {
        esgDesc = '🌟 非常环保';
    } else if (sustainable_score >= 70) {
        esgDesc = '🌿 较为环保';
    } else {
        esgDesc = '⚡ 能耗中等';
    }
    
    return `
${alert_emoji} *${protocol} 风险分析*

*风险评分:* \`${risk_score}/100\`
*风险等级:* ${alert_level.toUpperCase()}
*评估:* ${riskDesc}

*绿色评分:* \`${sustainable_score}/100\` ${esgDesc}

*链上指标:*
• 24h交易量: $${(metrics.volume_24h / 1000000).toFixed(2)}M
• 流动性变化: ${(metrics.liquidity_change * 100).toFixed(1)}%
• 鲸鱼转移: ${metrics.whale_transfers}次
• 持有集中度: ${(metrics.holder_concentration * 100).toFixed(1)}%

*更新时间:* ${new Date(timestamp).toLocaleString('zh-CN')}

${risk_score > 70 ? '\n⚠️ *建议: 考虑降低仓位或撤离*' : ''}
    `.trim();
}

/**
 * 广播警报给所有订阅者
 */
async function broadcastAlert(protocol, riskScore) {
    if (subscribers.size === 0) return;
    
    const alertMessage = `
🚨 *高风险警报!*

*协议:* ${protocol}
*风险分数:* ${riskScore}/100

建议立即检查您的持仓并考虑撤离!

查看详情: /risk ${protocol}
    `;
    
    for (const chatId of subscribers) {
        try {
            await bot.telegram.sendMessage(chatId, alertMessage, { parse_mode: 'Markdown' });
            console.log(`📤 警报已发送至: ${chatId}`);
        } catch (error) {
            console.error(`发送警报失败 (${chatId}):`, error.message);
        }
    }
}

// ==================== 定时任务（可选）====================

// 每5分钟检查一次所有协议（可选功能）
const cron = require('node-cron');

cron.schedule('*/5 * * * *', async () => {
    if (subscribers.size === 0) return;
    
    console.log('⏰ 执行定时风险检查...');
    
    const protocols = ['Jupiter', 'Orca', 'Raydium', 'Serum'];
    
    for (const protocol of protocols) {
        try {
            const response = await axios.get(`${API_BASE}/api/predict_risk`, {
                params: { protocol }
            });
            
            const { risk_score } = response.data;
            
            // 如果风险分数>80，发送警报
            if (risk_score > 80) {
                await broadcastAlert(protocol, risk_score);
            }
            
        } catch (error) {
            console.error(`检查 ${protocol} 失败:`, error.message);
        }
    }
});

// ==================== 错误处理 ====================

bot.catch((err, ctx) => {
    console.error(`❌ Bot错误 [${ctx.updateType}]:`, err);
    ctx.reply('抱歉，处理您的请求时出现错误，请稍后重试。');
});

// ==================== 启动Bot ====================

async function startBot() {
    console.log('🚀 启动 Prophet Sentinel Bot...');
    console.log(`📡 API地址: ${API_BASE}`);
    
    try {
        await bot.launch({
            dropPendingUpdates: true // 忽略启动前的旧消息
        });
        
        console.log('✅ Bot已启动! 等待消息...\n');
        console.log('可用命令:');
        console.log('  /start - 开始');
        console.log('  /risk <协议> - 查询风险');
        console.log('  /protocols - 协议列表');
        console.log('  /subscribe - 订阅警报');
        console.log('  /help - 帮助\n');
        
        console.log('💡 提示: 如果无法连接，请检查:');
        console.log('   1. 网络连接是否正常');
        console.log('   2. 是否需要配置代理 (TELEGRAM_PROXY_HOST/PORT)');
        console.log('   3. Bot Token是否正确\n');
        
    } catch (err) {
        console.error('❌ Bot启动失败:', err.message);
        
        if (err.code === 'ETIMEDOUT' || err.code === 'ENOTFOUND') {
            console.error('\n🌐 网络连接问题:');
            console.error('   - 无法连接到 api.telegram.org');
            console.error('   - 请检查网络连接或配置代理');
            console.error('   - 在.env中添加: TELEGRAM_PROXY_HOST 和 TELEGRAM_PROXY_PORT\n');
        } else if (err.response && err.response.error_code === 401) {
            console.error('\n🔑 Token错误:');
            console.error('   - Bot Token无效或已过期');
            console.error('   - 请在 @BotFather 检查Token\n');
        }
        
        console.log('⚠️  Bot将继续尝试运行，但可能无法正常工作...\n');
        // 不退出进程，让用户可以看到错误信息
    }
}

startBot();

// 优雅退出
process.once('SIGINT', () => {
    console.log('\n👋 停止Bot...');
    bot.stop('SIGINT');
});

process.once('SIGTERM', () => {
    console.log('\n👋 停止Bot...');
    bot.stop('SIGTERM');
});




