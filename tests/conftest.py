"""
pytest 配置文件
配置测试环境、fixtures 和钩子函数

Prophet Sentinel Test Suite Configuration
"""
import pytest
import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

# ==================== 路径配置 | Path Configuration ====================
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_path = os.path.join(project_root, 'backend')

# 确保路径在 sys.path 中
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ==================== 环境配置 | Environment Configuration ====================
os.environ['TESTING'] = 'true'
os.environ['FLASK_ENV'] = 'testing'
os.environ['FLASK_DEBUG'] = 'false'

# ==================== 日志配置 | Logging Configuration ====================
# 减少测试期间的日志噪音
logging.getLogger('prophet-sentinel').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# ==================== Pytest 钩子 | Pytest Hooks ====================

def pytest_configure(config):
    """Pytest 配置钩子"""
    # 创建测试日志目录
    logs_dir = os.path.join(project_root, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # 设置测试开始时间
    config.test_start_time = datetime.now()


def pytest_sessionstart(session):
    """测试会话开始时调用"""
    print("\n" + "="*70)
    print("🧪 Prophet Sentinel Test Suite")
    print("="*70)


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时调用"""
    print("\n" + "="*70)
    print(f"✨ 测试完成 | Exit Status: {exitstatus}")
    print("="*70)


def pytest_collection_modifyitems(config, items):
    """修改收集到的测试项"""
    # 自动为测试添加标记
    for item in items:
        # 根据文件名添加标记
        if "test_api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
            item.add_marker(pytest.mark.integration)
        elif "test_model" in str(item.fspath):
            item.add_marker(pytest.mark.model)
            item.add_marker(pytest.mark.unit)


# ==================== 路径 Fixtures | Path Fixtures ====================

@pytest.fixture(scope='session')
def project_root_dir():
    """返回项目根目录路径"""
    return project_root


@pytest.fixture(scope='session')
def backend_dir():
    """返回 backend 目录路径"""
    return backend_path


@pytest.fixture(scope='session')
def tests_dir():
    """返回测试目录路径"""
    return os.path.join(project_root, 'tests')


@pytest.fixture(scope='session')
def test_data_dir(tests_dir):
    """返回测试数据目录路径"""
    data_dir = os.path.join(tests_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


# ==================== 测试数据 Fixtures | Test Data Fixtures ====================

@pytest.fixture
def sample_protocol_data():
    """提供示例协议数据"""
    return {
        'protocol': 'Jupiter',
        'volume_24h': 50000000,
        'liquidity_change': 0.1,
        'whale_transfers': 2,
        'holder_concentration': 0.35
    }


@pytest.fixture
def high_risk_protocol_data():
    """提供高风险协议数据"""
    return {
        'protocol': 'HighRiskProtocol',
        'volume_24h': 1000000,
        'liquidity_change': -0.5,
        'whale_transfers': 15,
        'holder_concentration': 0.95
    }


@pytest.fixture
def low_risk_protocol_data():
    """提供低风险协议数据"""
    return {
        'protocol': 'LowRiskProtocol',
        'volume_24h': 100000000,
        'liquidity_change': 0.2,
        'whale_transfers': 1,
        'holder_concentration': 0.15
    }


@pytest.fixture
def protocol_list():
    """提供协议列表"""
    return ['Jupiter', 'Orca', 'Raydium', 'Serum', 'Marinade', 'Solend']


# ==================== 工具 Fixtures | Utility Fixtures ====================

@pytest.fixture
def temp_file(tmp_path):
    """创建临时文件"""
    def _create_temp_file(filename, content=""):
        file_path = tmp_path / filename
        file_path.write_text(content)
        return str(file_path)
    return _create_temp_file


@pytest.fixture
def json_file(tmp_path):
    """创建临时 JSON 文件"""
    def _create_json_file(filename, data):
        file_path = tmp_path / filename
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return str(file_path)
    return _create_json_file


# ==================== 性能测试 Fixtures | Performance Test Fixtures ====================

@pytest.fixture
def timer():
    """测试执行时间计时器"""
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            
        def start(self):
            self.start_time = datetime.now()
            
        def stop(self):
            self.end_time = datetime.now()
            
        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time).total_seconds()
            return None
    
    return Timer()


# ==================== Mock Fixtures ====================

@pytest.fixture
def mock_solana_response():
    """Mock Solana RPC 响应"""
    return {
        'jsonrpc': '2.0',
        'result': {
            'value': 1000000000,  # 1 SOL in lamports
        },
        'id': 1
    }


# ==================== 清理 Fixtures | Cleanup Fixtures ====================

@pytest.fixture(autouse=True)
def reset_environment():
    """每个测试后重置环境"""
    yield
    # 测试后清理逻辑
    pass


@pytest.fixture(scope="session", autouse=True)
def cleanup_logs():
    """测试会话结束后清理旧日志"""
    yield
    # 可以在这里添加清理旧日志文件的逻辑
    pass








