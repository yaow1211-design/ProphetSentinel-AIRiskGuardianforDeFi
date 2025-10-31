# 🧪 测试指南 | Testing Guide

## 📋 概述 | Overview

Prophet Sentinel 的测试套件已经过优化和修复，现在可以正常运行。

### ✅ 已修复的问题 | Fixed Issues

1. ✅ **目录结构问题** - 添加了缺失的 `__init__.py` 文件
2. ✅ **路径导入问题** - 配置了正确的 Python 路径
3. ✅ **虚拟环境支持** - 创建了使用虚拟环境的测试脚本
4. ✅ **服务初始化** - 修复了测试中的服务初始化问题

---

## 🚀 快速开始 | Quick Start

### 方法1: 使用测试脚本（推荐）| Use Test Script (Recommended)

```bash
# 运行所有测试
./run_tests.sh

# 或者
bash run_tests.sh all

# 快速测试（遇到第一个失败就停止）
./run_tests.sh quick

# 只测试 API
./run_tests.sh api

# 只测试 ML 模型
./run_tests.sh model

# 生成覆盖率报告
./run_tests.sh cov
```

### 方法2: 使用 pytest 命令 | Use pytest Commands

```bash
# 激活虚拟环境
cd backend
source venv/bin/activate

# 返回项目根目录
cd ..

# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_api.py -v
pytest tests/test_model.py -v

# 运行特定测试函数
pytest tests/test_api.py::test_predict_risk -v

# 显示详细输出
pytest tests/ -v --tb=long

# 生成覆盖率报告
pytest tests/ --cov=backend --cov-report=html
```

---

## 📁 项目结构 | Project Structure

```
ProphetSentinel-AIRiskGuardianforDeFi/
├── backend/
│   ├── __init__.py           ✨ 新增
│   ├── app.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py       ✨ 新增
│   │   ├── predict.py
│   │   └── train_model.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── solana_service.py
│   │   └── sustainability.py
│   ├── utils/
│   │   ├── __init__.py       ✨ 新增
│   │   └── logger.py
│   └── venv/
├── tests/
│   ├── conftest.py           ✨ 已更新
│   ├── test_api.py           ✨ 已更新
│   └── test_model.py         ✨ 已更新
├── pytest.ini                ✨ 新增
├── setup.py                  ✨ 新增
└── run_tests.sh              ✨ 新增
```

---

## 🔧 配置文件说明 | Configuration Files

### `pytest.ini`

配置 pytest 的行为：
- Python 路径设置
- 测试发现模式
- 输出选项
- 标记定义

### `setup.py`

Python 包配置：
- 定义包结构
- 声明依赖
- 开发环境配置

### `conftest.py`

pytest 配置和 fixtures：
- 设置 Python 路径
- 环境变量配置
- 共享 fixtures

---

## 📊 测试覆盖 | Test Coverage

### API 测试 (`test_api.py`)

- ✅ `test_home` - 测试 API 首页
- ✅ `test_health_check` - 测试健康检查端点
- ✅ `test_predict_risk` - 测试风险预测功能
- ✅ `test_protocols_list` - 测试协议列表
- ✅ `test_verify_proof` - 测试 zk 隐私验证
- ✅ `test_invalid_endpoint` - 测试无效端点处理

### ML 模型测试 (`test_model.py`)

- ✅ `test_risk_predictor_init` - 测试预测器初始化
- ✅ `test_predict_low_risk` - 测试低风险预测
- ✅ `test_predict_high_risk` - 测试高风险预测
- ✅ `test_predict_with_zero_values` - 测试零值输入

### 当前测试结果

```
10 passed, 1 warning ✅
100% 测试通过率
```

---

## 🛠️ 故障排除 | Troubleshooting

### 问题1: ModuleNotFoundError

**错误信息:**
```
ModuleNotFoundError: No module named 'flask_cors'
```

**解决方案:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 问题2: 路径导入错误

**错误信息:**
```
ImportError: cannot import name 'app' from 'app'
```

**解决方案:**
确保使用正确的 Python 路径：
```bash
export PYTHONPATH="${PWD}:${PWD}/backend:${PYTHONPATH}"
```

或者使用 `run_tests.sh` 脚本，它会自动设置路径。

### 问题3: 服务未初始化

**错误信息:**
```
'NoneType' object has no attribute 'get_protocol_metrics'
```

**解决方案:**
已在 `test_api.py` 的 `client` fixture 中修复。确保你使用的是更新后的版本。

### 问题4: pytest 未安装

**解决方案:**
```bash
cd backend
source venv/bin/activate
pip install pytest pytest-cov
```

---

## 🔍 开发测试流程 | Development Testing Workflow

### 1. 修改代码前

```bash
# 运行所有测试确保基线正常
./run_tests.sh
```

### 2. 开发过程中

```bash
# 运行快速测试（TDD模式）
./run_tests.sh quick

# 或只运行相关测试
pytest tests/test_api.py::test_predict_risk -v
```

### 3. 提交代码前

```bash
# 运行完整测试套件
./run_tests.sh all

# 检查覆盖率
./run_tests.sh cov

# 确保所有测试通过后再提交
git add .
git commit -m "your changes"
```

---

## 📈 添加新测试 | Adding New Tests

### 创建新测试文件

```python
# tests/test_new_feature.py
"""
新功能测试
"""
import pytest
from your_module import YourClass

def test_new_feature():
    """测试新功能"""
    result = YourClass().new_method()
    assert result == expected_value
```

### 使用 fixtures

```python
@pytest.fixture
def sample_data():
    """提供测试数据"""
    return {"key": "value"}

def test_with_fixture(sample_data):
    """使用 fixture 的测试"""
    assert sample_data["key"] == "value"
```

### 添加标记

```python
@pytest.mark.slow
def test_slow_operation():
    """标记为慢速测试"""
    pass

@pytest.mark.integration
def test_integration():
    """标记为集成测试"""
    pass
```

运行特定标记的测试：
```bash
pytest -m slow     # 只运行慢速测试
pytest -m unit     # 只运行单元测试
```

---

## 🌐 CI/CD 集成 | CI/CD Integration

### GitHub Actions 示例

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          chmod +x run_tests.sh
          ./run_tests.sh cov
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 📚 参考资料 | References

- [Pytest 文档](https://docs.pytest.org/)
- [Flask Testing 指南](https://flask.palletsprojects.com/en/latest/testing/)
- [Python unittest 模块](https://docs.python.org/3/library/unittest.html)

---

## ✅ 检查清单 | Checklist

在提交 PR 之前，请确保：

- [ ] 所有测试通过 (`./run_tests.sh`)
- [ ] 新功能有对应的测试
- [ ] 测试覆盖率 ≥ 80%
- [ ] 代码符合 PEP8 规范
- [ ] 更新了相关文档

---

## 💡 最佳实践 | Best Practices

1. **编写可维护的测试**
   - 使用描述性的测试名称
   - 一个测试只测试一个功能点
   - 使用 fixtures 减少重复代码

2. **保持测试快速**
   - 使用 mock 代替真实的外部调用
   - 并行运行测试 (`pytest -n auto`)

3. **测试覆盖率**
   - 目标：≥ 80% 覆盖率
   - 关注核心业务逻辑
   - 不要为了覆盖率而写无意义的测试

4. **持续集成**
   - 每次提交都运行测试
   - 在 CI 中生成覆盖率报告
   - 不允许合并失败的测试

---

**🎉 测试环境已完全修复，可以正常使用！**

有问题请查看 [QUICKSTART.md](QUICKSTART.md) 或联系维护团队。

