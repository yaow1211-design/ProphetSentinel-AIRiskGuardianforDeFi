"""
pytest配置文件
配置测试环境和fixture
"""
import pytest
import sys
import os

# 添加项目路径到sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_path = os.path.join(project_root, 'backend')

# 确保backend路径在sys.path中
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 设置环境变量，用于测试模式
os.environ['TESTING'] = 'true'
os.environ['FLASK_ENV'] = 'testing'

@pytest.fixture(scope='session')
def project_root_dir():
    """返回项目根目录路径"""
    return project_root

@pytest.fixture(scope='session')
def backend_dir():
    """返回backend目录路径"""
    return backend_path








