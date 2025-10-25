"""
ML模型测试
"""
import pytest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

from models.predict import RiskPredictor

def test_risk_predictor_init():
    """测试预测器初始化"""
    predictor = RiskPredictor(demo_mode=True)
    assert predictor is not None
    assert predictor.demo_mode == True

def test_predict_low_risk():
    """测试低风险预测"""
    predictor = RiskPredictor(demo_mode=True)
    
    metrics = {
        'volume_24h': 50000000,
        'liquidity_change': 0.1,  # 正向变化
        'whale_transfers': 1,      # 少量转移
        'holder_concentration': 0.3  # 低集中度
    }
    
    result = predictor.predict(metrics)
    
    assert 'risk_score' in result
    assert 'confidence' in result
    assert 0 <= result['risk_score'] <= 100
    assert 0 <= result['confidence'] <= 1

def test_predict_high_risk():
    """测试高风险预测"""
    predictor = RiskPredictor(demo_mode=True)
    
    metrics = {
        'volume_24h': 1000000,
        'liquidity_change': -0.4,  # 大幅下降
        'whale_transfers': 10,      # 频繁转移
        'holder_concentration': 0.9  # 高集中度
    }
    
    result = predictor.predict(metrics)
    
    assert result['risk_score'] > 50  # 应该是高风险

def test_predict_with_zero_values():
    """测试零值输入"""
    predictor = RiskPredictor(demo_mode=True)
    
    metrics = {
        'volume_24h': 0,
        'liquidity_change': 0,
        'whale_transfers': 0,
        'holder_concentration': 0
    }
    
    result = predictor.predict(metrics)
    assert 'risk_score' in result


