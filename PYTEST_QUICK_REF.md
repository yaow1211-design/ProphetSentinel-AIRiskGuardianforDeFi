# 🚀 Pytest 快速参考 | Quick Reference

## 📋 常用命令 | Common Commands

```bash
# 基本测试
pytest tests/ -v                    # 运行所有测试（详细输出）
./run_tests.sh                     # 使用测试脚本

# 按标记运行
pytest -m unit                     # 只运行单元测试
pytest -m api                      # 只运行 API 测试
pytest -m smoke                    # 只运行冒烟测试
pytest -m "not slow"               # 排除慢速测试

# 覆盖率
pytest --cov                       # 生成覆盖率报告
pytest --cov --cov-report=html     # HTML 覆盖率报告

# 调试
pytest -s                          # 显示打印输出
pytest --pdb                       # 失败时调试
pytest -x                          # 第一个失败后停止
pytest --lf                        # 只运行上次失败的测试

# 性能
pytest --durations=5               # 显示最慢的 5 个测试
```

---

## 🏷️ 测试标记 | Test Markers

| 标记 | 用途 | 示例 |
|------|------|------|
| `unit` | 单元测试 | `@pytest.mark.unit` |
| `integration` | 集成测试 | `@pytest.mark.integration` |
| `api` | API 测试 | `@pytest.mark.api` |
| `model` | 模型测试 | `@pytest.mark.model` |
| `smoke` | 冒烟测试 | `@pytest.mark.smoke` |
| `slow` | 慢速测试 | `@pytest.mark.slow` |

---

## 🛠️ 辅助工具 | Helper Tools

### APITestHelper
```python
from test_helpers import APITestHelper

api_helper = APITestHelper()
data = api_helper.assert_valid_api_response(response)
api_helper.assert_risk_prediction_format(data)
```

### ModelTestHelper
```python
from test_helpers import ModelTestHelper

model_helper = ModelTestHelper()
model_helper.assert_valid_prediction(prediction)
```

### TestDataBuilder
```python
from test_helpers import TestDataBuilder

builder = TestDataBuilder()
metrics = builder.build_protocol_metrics(protocol="Jupiter")
```

---

## 📦 常用 Fixtures

```python
def test_example(
    client,                    # Flask 测试客户端
    sample_protocol_data,      # 示例协议数据
    test_data_dir,            # 测试数据目录
    timer,                    # 性能计时器
    temp_file                 # 临时文件创建器
):
    pass
```

---

## 📊 覆盖率命令

```bash
# 基本覆盖率
pytest --cov=backend

# HTML 报告
pytest --cov=backend --cov-report=html
open htmlcov/index.html

# 显示缺失的行
pytest --cov=backend --cov-report=term-missing

# 最低覆盖率要求（60%）
pytest --cov=backend --cov-fail-under=60
```

---

## 🎯 实用技巧 | Tips

### 只运行特定测试
```bash
pytest tests/test_api.py::test_predict_risk -v
```

### 运行匹配名称的测试
```bash
pytest -k "predict" -v          # 名称包含 predict 的测试
pytest -k "not slow" -v         # 名称不包含 slow 的测试
```

### 并行测试（需要 pytest-xdist）
```bash
pytest -n auto                  # 自动使用所有 CPU
pytest -n 4                     # 使用 4 个进程
```

### 生成 JUnit XML（CI/CD）
```bash
pytest --junitxml=report.xml
```

---

## 🔍 常见问题 | FAQ

**Q: 如何只运行失败的测试？**
```bash
pytest --lf
```

**Q: 如何查看打印输出？**
```bash
pytest -s
```

**Q: 如何在失败时停止？**
```bash
pytest -x
```

**Q: 如何查看所有标记？**
```bash
pytest --markers
```

---

## 📁 项目结构 | Structure

```
tests/
├── conftest.py           # fixtures 和配置
├── test_helpers.py       # 辅助工具
├── test_api.py          # API 测试
├── test_model.py        # 模型测试
└── data/                # 测试数据
    ├── README.md
    └── sample_protocols.json
```

---

## 🎨 编写测试模板

### API 测试模板
```python
@pytest.mark.api
@pytest.mark.integration
def test_api_endpoint(client):
    """测试 API 端点"""
    response = client.get('/api/endpoint')
    data = api_helper.assert_valid_api_response(response)
    assert data['key'] == 'value'
```

### 模型测试模板
```python
@pytest.mark.model
@pytest.mark.unit
def test_model_function():
    """测试模型功能"""
    result = model_function(input_data)
    model_helper.assert_valid_prediction(result)
```

### 性能测试模板
```python
def test_performance(timer):
    """测试性能"""
    timer.start()
    # 执行操作
    timer.stop()
    assert timer.elapsed < 2.0
```

---

**💡 提示**: 查看完整文档 [PYTEST_OPTIMIZATION.md](PYTEST_OPTIMIZATION.md)

**🎯 快速开始**: `pytest tests/ -m smoke -v`

