"""
测试辅助工具类
Test Helper Utilities for Prophet Sentinel
"""
import json
import time
from typing import Dict, Any, List
from contextlib import contextmanager


class TestDataBuilder:
    """测试数据构建器"""
    
    @staticmethod
    def build_protocol_metrics(
        protocol: str = "TestProtocol",
        volume_24h: float = 10000000,
        liquidity_change: float = 0.0,
        whale_transfers: int = 5,
        holder_concentration: float = 0.5
    ) -> Dict[str, Any]:
        """构建协议指标数据"""
        return {
            'protocol': protocol,
            'volume_24h': volume_24h,
            'liquidity_change': liquidity_change,
            'whale_transfers': whale_transfers,
            'holder_concentration': holder_concentration
        }
    
    @staticmethod
    def build_risk_prediction(
        risk_score: int = 50,
        confidence: float = 0.85,
        alert_level: str = "medium"
    ) -> Dict[str, Any]:
        """构建风险预测结果"""
        return {
            'risk_score': risk_score,
            'confidence': confidence,
            'alert_level': alert_level
        }


class APITestHelper:
    """API 测试辅助类"""
    
    @staticmethod
    def assert_valid_api_response(response, expected_status=200):
        """验证 API 响应格式"""
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"
        
        data = response.get_json()
        assert data is not None, "Response should contain JSON data"
        return data
    
    @staticmethod
    def assert_risk_prediction_format(data: Dict[str, Any]):
        """验证风险预测响应格式"""
        required_fields = [
            'protocol', 'risk_score', 'alert_level', 
            'sustainable_score', 'timestamp'
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # 验证数据类型
        assert isinstance(data['risk_score'], (int, float)), \
            "risk_score should be a number"
        assert 0 <= data['risk_score'] <= 100, \
            "risk_score should be between 0 and 100"
        assert isinstance(data['sustainable_score'], (int, float)), \
            "sustainable_score should be a number"
    
    @staticmethod
    def assert_error_response(response, expected_status=500):
        """验证错误响应格式"""
        assert response.status_code == expected_status
        data = response.get_json()
        assert 'error' in data or 'message' in data, \
            "Error response should contain error or message field"


class ModelTestHelper:
    """模型测试辅助类"""
    
    @staticmethod
    def assert_valid_prediction(prediction: Dict[str, Any]):
        """验证模型预测结果"""
        assert 'risk_score' in prediction, "Prediction should have risk_score"
        assert isinstance(prediction['risk_score'], (int, float)), \
            "risk_score should be numeric"
        assert 0 <= prediction['risk_score'] <= 100, \
            "risk_score should be between 0 and 100"
    
    @staticmethod
    def calculate_prediction_accuracy(predictions: List[Dict], actuals: List[int]) -> float:
        """计算预测准确率"""
        if len(predictions) != len(actuals):
            raise ValueError("Predictions and actuals must have same length")
        
        correct = sum(
            1 for pred, actual in zip(predictions, actuals)
            if abs(pred['risk_score'] - actual) < 10  # 允许 10 分误差
        )
        return correct / len(predictions) if predictions else 0.0


class PerformanceTestHelper:
    """性能测试辅助类"""
    
    @staticmethod
    @contextmanager
    def measure_time(operation_name: str = "Operation"):
        """测量操作执行时间"""
        start = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start
            print(f"\n⏱️  {operation_name} took {elapsed:.3f}s")
    
    @staticmethod
    def assert_performance(elapsed_time: float, max_time: float, operation: str = "Operation"):
        """断言性能要求"""
        assert elapsed_time <= max_time, \
            f"{operation} took {elapsed_time:.3f}s, expected <= {max_time}s"


class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_protocol_name(protocol: str) -> bool:
        """验证协议名称"""
        if not protocol:
            return False
        if not isinstance(protocol, str):
            return False
        if len(protocol) < 2 or len(protocol) > 50:
            return False
        return True
    
    @staticmethod
    def validate_risk_score(score: Any) -> bool:
        """验证风险分数"""
        if not isinstance(score, (int, float)):
            return False
        if score < 0 or score > 100:
            return False
        return True
    
    @staticmethod
    def validate_metrics(metrics: Dict[str, Any]) -> tuple[bool, str]:
        """验证指标数据，返回 (是否有效, 错误消息)"""
        required_fields = ['volume_24h', 'liquidity_change', 'whale_transfers', 'holder_concentration']
        
        for field in required_fields:
            if field not in metrics:
                return False, f"Missing required field: {field}"
        
        # 验证数值范围
        if metrics['volume_24h'] < 0:
            return False, "volume_24h must be non-negative"
        
        if not -1.0 <= metrics['liquidity_change'] <= 1.0:
            return False, "liquidity_change should be between -1 and 1"
        
        if metrics['whale_transfers'] < 0:
            return False, "whale_transfers must be non-negative"
        
        if not 0.0 <= metrics['holder_concentration'] <= 1.0:
            return False, "holder_concentration should be between 0 and 1"
        
        return True, ""


class MockDataGenerator:
    """Mock 数据生成器"""
    
    @staticmethod
    def generate_protocols(count: int = 5) -> List[str]:
        """生成协议列表"""
        base_protocols = ['Jupiter', 'Orca', 'Raydium', 'Serum', 'Marinade', 'Solend']
        return base_protocols[:count] + [f"Protocol_{i}" for i in range(max(0, count - len(base_protocols)))]
    
    @staticmethod
    def generate_random_metrics() -> Dict[str, Any]:
        """生成随机指标数据"""
        import random
        return {
            'volume_24h': random.uniform(1000000, 100000000),
            'liquidity_change': random.uniform(-0.3, 0.3),
            'whale_transfers': random.randint(0, 20),
            'holder_concentration': random.uniform(0.1, 0.9)
        }


class TestReporter:
    """测试报告器"""
    
    def __init__(self):
        self.results = []
    
    def add_result(self, test_name: str, passed: bool, duration: float = 0.0, message: str = ""):
        """添加测试结果"""
        self.results.append({
            'test': test_name,
            'passed': passed,
            'duration': duration,
            'message': message
        })
    
    def summary(self) -> str:
        """生成测试摘要"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        failed = total - passed
        
        return f"""
测试摘要 | Test Summary
========================
总计 Total: {total}
通过 Passed: {passed}
失败 Failed: {failed}
成功率 Pass Rate: {(passed/total*100) if total > 0 else 0:.1f}%
        """
    
    def export_json(self, filepath: str):
        """导出为 JSON"""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)


# ==================== 辅助函数 | Helper Functions ====================

def compare_dicts(dict1: Dict, dict2: Dict, ignore_keys: List[str] = None) -> bool:
    """比较两个字典，可忽略特定键"""
    ignore_keys = ignore_keys or []
    
    keys1 = set(dict1.keys()) - set(ignore_keys)
    keys2 = set(dict2.keys()) - set(ignore_keys)
    
    if keys1 != keys2:
        return False
    
    for key in keys1:
        if dict1[key] != dict2[key]:
            return False
    
    return True


def load_test_data(filename: str) -> Any:
    """从文件加载测试数据"""
    import os
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
    filepath = os.path.join(test_data_dir, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Test data file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        if filename.endswith('.json'):
            return json.load(f)
        else:
            return f.read()


def create_test_data_file(filename: str, data: Any):
    """创建测试数据文件"""
    import os
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(test_data_dir, exist_ok=True)
    
    filepath = os.path.join(test_data_dir, filename)
    
    with open(filepath, 'w') as f:
        if isinstance(data, (dict, list)):
            json.dump(data, f, indent=2)
        else:
            f.write(str(data))
    
    return filepath

