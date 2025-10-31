# 测试数据目录 | Test Data Directory

这个目录包含测试所需的样本数据文件。

## 文件说明 | File Description

### `sample_protocols.json`
包含各种协议的样本指标数据，用于测试风险预测功能。

**结构:**
```json
{
  "protocols": [
    {
      "name": "协议名称",
      "type": "协议类型",
      "metrics": {
        "volume_24h": "24小时交易量",
        "liquidity_change": "流动性变化",
        "whale_transfers": "鲸鱼转账次数",
        "holder_concentration": "持有集中度"
      },
      "expected_risk": "预期风险等级 (low/medium/high)"
    }
  ]
}
```

## 使用方法 | Usage

### Python 中加载数据
```python
import json
import os

def load_test_protocols():
    data_file = os.path.join(os.path.dirname(__file__), 'data', 'sample_protocols.json')
    with open(data_file, 'r') as f:
        return json.load(f)

protocols = load_test_protocols()
```

### 使用 conftest fixtures
```python
def test_with_sample_data(test_data_dir):
    filepath = os.path.join(test_data_dir, 'sample_protocols.json')
    with open(filepath, 'r') as f:
        data = json.load(f)
    # 使用数据进行测试
```

## 添加新数据 | Adding New Data

1. 创建新的 JSON 文件
2. 遵循现有的数据结构
3. 在测试中使用 `load_test_data()` 辅助函数加载

## 注意事项 | Notes

- 不要提交真实的生产数据到此目录
- 保持数据文件小而简洁
- 使用描述性的文件名
- 添加适当的注释说明数据用途

