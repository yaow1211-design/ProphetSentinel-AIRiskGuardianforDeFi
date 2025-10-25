"""
API端点测试
"""
import pytest
import sys
import os

# 添加backend到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

from app import app

@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """测试首页"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Prophet Sentinel API'

def test_health_check(client):
    """测试健康检查"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_predict_risk(client):
    """测试风险预测"""
    response = client.get('/api/predict_risk?protocol=Jupiter')
    assert response.status_code == 200
    data = response.get_json()
    
    assert 'protocol' in data
    assert 'risk_score' in data
    assert 'sustainable_score' in data
    assert data['protocol'] == 'Jupiter'
    assert 0 <= data['risk_score'] <= 100
    assert 0 <= data['sustainable_score'] <= 100

def test_protocols_list(client):
    """测试协议列表"""
    response = client.get('/api/protocols')
    assert response.status_code == 200
    data = response.get_json()
    
    assert 'protocols' in data
    assert len(data['protocols']) > 0

def test_verify_proof(client):
    """测试zk验证"""
    response = client.post('/api/verify_proof',
        json={
            'wallet_hash': 'test123',
            'risk_score': 75
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    
    assert 'verified' in data
    assert 'proof_hash' in data

def test_invalid_endpoint(client):
    """测试无效端点"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404


