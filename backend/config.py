"""
配置管理模块
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-prod')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    PORT = int(os.getenv('FLASK_PORT', 5001))
    
    # Solana配置
    SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL', 'https://api.mainnet-beta.solana.com')
    SOLANA_NETWORK = os.getenv('SOLANA_NETWORK', 'mainnet-beta')
    HELIUS_API_KEY = os.getenv('HELIUS_API_KEY', '')
    
    # Telegram配置
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID', '')
    
    # 模型配置
    MODEL_PATH = 'backend/models/risk_model.pkl'
    MODEL_UPDATE_INTERVAL = 3600  # 1小时
    
    # API配置
    API_RATE_LIMIT = 100  # 每分钟请求数
    CACHE_TIMEOUT = 60  # 缓存过期时间（秒）
    
    # 风险阈值
    RISK_THRESHOLD_LOW = 30
    RISK_THRESHOLD_MEDIUM = 70
    RISK_THRESHOLD_HIGH = 90



