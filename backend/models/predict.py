"""
ML模型推理模块
"""
import os
import pickle
import numpy as np
from typing import Dict
import logging

logger = logging.getLogger('prophet-sentinel')

class RiskPredictor:
    """风险预测器类"""
    
    def __init__(self, model_path='backend/models/risk_model.pkl', demo_mode=False):
        """
        初始化预测器
        
        Args:
            model_path: 模型文件路径
            demo_mode: 演示模式（使用模拟数据）
        """
        self.model_path = model_path
        self.demo_mode = demo_mode
        self.model = None
        
        if not demo_mode:
            self._load_model()
        else:
            logger.warning("⚠️ 运行在演示模式，使用模拟预测")
    
    def _load_model(self):
        """加载训练好的模型"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"✅ 模型加载成功: {self.model_path}")
            else:
                logger.warning(f"⚠️ 模型文件不存在: {self.model_path}，切换到演示模式")
                self.demo_mode = True
        except Exception as e:
            logger.error(f"❌ 模型加载失败: {e}")
            self.demo_mode = True
    
    def predict(self, metrics: Dict) -> Dict:
        """
        预测风险分数
        
        Args:
            metrics: 协议指标字典
                {
                    'volume_24h': float,
                    'liquidity_change': float,
                    'whale_transfers': int,
                    'holder_concentration': float
                }
        
        Returns:
            预测结果字典
                {
                    'risk_score': int (0-100),
                    'confidence': float (0-1)
                }
        """
        if self.demo_mode:
            return self._demo_predict(metrics)
        
        try:
            # 准备特征向量
            features = self._prepare_features(metrics)
            
            # 模型预测
            proba = self.model.predict_proba([features])[0]
            
            # 转换为0-100分数
            risk_score = int(proba[1] * 100)
            confidence = float(np.max(proba))
            
            return {
                'risk_score': risk_score,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"❌ 预测失败: {e}")
            return self._demo_predict(metrics)
    
    def _prepare_features(self, metrics: Dict) -> np.array:
        """
        准备模型输入特征
        
        特征顺序必须与训练时一致：
        [volume_24h, liquidity_change, whale_transfers, holder_concentration]
        """
        features = [
            float(metrics.get('volume_24h', 0)),
            float(metrics.get('liquidity_change', 0)),
            float(metrics.get('whale_transfers', 0)),
            float(metrics.get('holder_concentration', 0))
        ]
        
        return np.array(features)
    
    def _demo_predict(self, metrics: Dict) -> Dict:
        """
        演示模式预测（基于规则的简单算法）
        
        风险计算逻辑：
        - 流动性大幅下降 → 高风险
        - 鲸鱼频繁转移 → 高风险
        - 持有集中度高 → 高风险
        """
        liquidity_change = metrics.get('liquidity_change', 0)
        whale_transfers = metrics.get('whale_transfers', 0)
        holder_concentration = metrics.get('holder_concentration', 0)
        
        # 基础风险分数
        risk_score = 50
        
        # 流动性变化影响（-30%流动性 → +30分风险）
        if liquidity_change < 0:
            risk_score += abs(liquidity_change) * 100
        
        # 鲸鱼转移影响（每次+5分）
        risk_score += whale_transfers * 5
        
        # 持有集中度影响（高集中度→高风险）
        risk_score += holder_concentration * 30
        
        # 限制在0-100范围
        risk_score = int(np.clip(risk_score, 0, 100))
        
        # 模拟置信度
        confidence = 0.75 + np.random.random() * 0.15
        
        return {
            'risk_score': risk_score,
            'confidence': round(confidence, 2)
        }



