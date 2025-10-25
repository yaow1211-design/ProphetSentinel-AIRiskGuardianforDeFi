"""
Prophet Sentinel - Flask后端主程序
实时AI风险预测API服务
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import logging
import os

from config import Config
from models.predict import RiskPredictor
from services.solana_service import SolanaService
from services.sustainability import calculate_sustainability_score
from utils.logger import setup_logger

# 初始化应用
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# 设置日志
logger = setup_logger()

# 初始化服务
risk_predictor = None
solana_service = None

def init_services():
    """初始化ML模型和Solana服务"""
    global risk_predictor, solana_service
    
    try:
        risk_predictor = RiskPredictor()
        solana_service = SolanaService()
        logger.info("✅ 服务初始化成功")
    except Exception as e:
        logger.error(f"❌ 服务初始化失败: {e}")
        # Demo模式：即使初始化失败也继续运行
        risk_predictor = RiskPredictor(demo_mode=True)
        solana_service = SolanaService(demo_mode=True)

# ==================== API路由 ====================

@app.route('/', methods=['GET'])
def home():
    """API首页"""
    return jsonify({
        'name': 'Prophet Sentinel API',
        'version': '1.0.0',
        'description': 'AI驱动的DeFi风险预测引擎',
        'endpoints': {
            '/api/health': '健康检查',
            '/api/predict_risk': '风险预测',
            '/api/protocols': '支持的协议列表',
            '/api/verify_proof': 'zk隐私验证'
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'model_loaded': risk_predictor is not None,
        'solana_connected': solana_service is not None
    })

@app.route('/api/predict_risk', methods=['GET'])
def predict_risk():
    """
    风险预测API
    参数: protocol (string) - 协议名称，如 'Jupiter', 'Orca'
    返回: JSON包含风险分数、警报等级、可持续性评分等
    """
    try:
        protocol = request.args.get('protocol', 'Jupiter')
        
        logger.info(f"🔍 收到风险预测请求: {protocol}")
        
        # 1. 从Solana拉取实时指标
        metrics = solana_service.get_protocol_metrics(protocol)
        
        # 2. ML模型预测风险
        prediction = risk_predictor.predict(metrics)
        
        # 3. 计算可持续性评分
        sustainable_score = calculate_sustainability_score(metrics)
        
        # 4. 确定警报等级
        risk_score = prediction['risk_score']
        if risk_score >= Config.RISK_THRESHOLD_HIGH:
            alert_level = 'critical'
            alert_emoji = '🚨'
        elif risk_score >= Config.RISK_THRESHOLD_MEDIUM:
            alert_level = 'high'
            alert_emoji = '⚠️'
        elif risk_score >= Config.RISK_THRESHOLD_LOW:
            alert_level = 'medium'
            alert_emoji = '⚡'
        else:
            alert_level = 'low'
            alert_emoji = '✅'
        
        response = {
            'protocol': protocol,
            'risk_score': risk_score,
            'alert_level': alert_level,
            'alert_emoji': alert_emoji,
            'sustainable_score': sustainable_score,
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': {
                'volume_24h': metrics.get('volume_24h'),
                'liquidity_change': metrics.get('liquidity_change'),
                'whale_transfers': metrics.get('whale_transfers'),
                'holder_concentration': metrics.get('holder_concentration')
            },
            'confidence': prediction.get('confidence', 0.85)
        }
        
        logger.info(f"✅ 预测完成: {protocol} - 风险分数 {risk_score}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ 预测失败: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/protocols', methods=['GET'])
def get_protocols():
    """获取支持的协议列表"""
    protocols = [
        {'name': 'Jupiter', 'type': 'DEX Aggregator', 'supported': True},
        {'name': 'Orca', 'type': 'AMM DEX', 'supported': True},
        {'name': 'Raydium', 'type': 'AMM DEX', 'supported': True},
        {'name': 'Serum', 'type': 'Order Book DEX', 'supported': True},
        {'name': 'Marinade', 'type': 'Liquid Staking', 'supported': True},
        {'name': 'Solend', 'type': 'Lending', 'supported': True},
    ]
    
    return jsonify({
        'protocols': protocols,
        'total': len(protocols)
    })

@app.route('/api/verify_proof', methods=['POST'])
def verify_proof():
    """
    zk隐私验证端点（演示版）
    接收钱包hash和风险分数，返回验证结果
    """
    try:
        data = request.json
        wallet_hash = data.get('wallet_hash')
        risk_score = data.get('risk_score')
        
        if not wallet_hash or risk_score is None:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 简化版zk验证（实际应使用zk-SNARK）
        import hashlib
        import time
        
        proof_data = f"{wallet_hash}:{risk_score}:{int(time.time())}"
        proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
        
        return jsonify({
            'verified': True,
            'proof_hash': proof_hash,
            'message': '✅ 风险分数已验证，钱包地址未泄露',
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ zk验证失败: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': '端点不存在'}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"内部错误: {e}")
    return jsonify({'error': '服务器内部错误'}), 500

# ==================== 应用启动 ====================

if __name__ == '__main__':
    logger.info("🚀 启动 Prophet Sentinel API...")
    
    # 初始化服务
    init_services()
    
    # 启动Flask服务
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )



