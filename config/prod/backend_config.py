"""
Prophet Sentinel - 生产环境配置
"""
import os

class Config:
    # Flask配置
    DEBUG = False
    PORT = int(os.getenv('PORT', 5001))
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

    # API配置
    SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL', 'https://api.mainnet-beta.solana.com')
    HELIUS_API_KEY = os.getenv('HELIUS_API_KEY')  # 可选

    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/logs/backend/app.log'

    # 风险阈值
    RISK_THRESHOLD_LOW = 30
    RISK_THRESHOLD_MEDIUM = 60
    RISK_THRESHOLD_HIGH = 80

    # ML模型配置
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../backend/models/risk_model.pkl')
    DEMO_MODE = False  # 生产环境禁用演示模式