"""
API 端点测试
Tests for Prophet Sentinel API endpoints
"""
import pytest
from app import app, init_services
from test_helpers import APITestHelper

# 使用标记自动分类（在 conftest.py 中自动添加）
# @pytest.mark.api 和 @pytest.mark.integration 会自动添加

@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    
    # 初始化服务（会自动使用demo模式）
    with app.app_context():
        init_services()
    
    with app.test_client() as client:
        yield client

# 创建辅助工具实例
api_helper = APITestHelper()

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

@pytest.mark.smoke
def test_predict_risk(client):
    """测试风险预测"""
    response = client.get('/api/predict_risk?protocol=Jupiter')
    data = api_helper.assert_valid_api_response(response, 200)
    
    # 使用辅助函数验证响应格式
    api_helper.assert_risk_prediction_format(data)
    
    # 额外的业务逻辑验证
    assert data['protocol'] == 'Jupiter'

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








