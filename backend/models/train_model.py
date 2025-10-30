"""
ML模型训练脚本
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_synthetic_training_data(n_samples=1000):
    """
    生成合成训练数据
    
    特征:
    - volume_24h: 24小时交易量
    - liquidity_change: 流动性变化率
    - whale_transfers: 鲸鱼转移次数
    - holder_concentration: 持有集中度
    
    标签:
    - 0: 低风险
    - 1: 高风险
    """
    logger.info(f"🔧 生成 {n_samples} 条合成训练数据...")
    
    np.random.seed(42)
    
    data = []
    
    for _ in range(n_samples):
        # 随机决定是否为高风险协议
        is_high_risk = np.random.rand() > 0.7  # 30%高风险
        
        if is_high_risk:
            # 高风险协议特征
            volume = np.random.uniform(1000000, 10000000)
            liquidity_change = np.random.uniform(-0.5, -0.1)  # 流动性下降
            whale_transfers = np.random.randint(5, 15)  # 频繁鲸鱼活动
            holder_concentration = np.random.uniform(0.7, 0.95)  # 高集中度
            label = 1
        else:
            # 低风险协议特征
            volume = np.random.uniform(5000000, 100000000)
            liquidity_change = np.random.uniform(-0.1, 0.3)  # 流动性稳定或增长
            whale_transfers = np.random.randint(0, 5)  # 少量鲸鱼活动
            holder_concentration = np.random.uniform(0.2, 0.6)  # 分散持有
            label = 0
        
        data.append({
            'volume_24h': volume,
            'liquidity_change': liquidity_change,
            'whale_transfers': whale_transfers,
            'holder_concentration': holder_concentration,
            'risk_label': label
        })
    
    df = pd.DataFrame(data)
    logger.info(f"✅ 数据生成完成: {len(df)} 条记录")
    logger.info(f"   高风险样本: {sum(df['risk_label'] == 1)} ({sum(df['risk_label'] == 1)/len(df)*100:.1f}%)")
    logger.info(f"   低风险样本: {sum(df['risk_label'] == 0)} ({sum(df['risk_label'] == 0)/len(df)*100:.1f}%)")
    
    return df

def train_risk_model(df):
    """训练RandomForest模型"""
    logger.info("🤖 开始训练模型...")
    
    # 准备特征和标签
    feature_columns = ['volume_24h', 'liquidity_change', 'whale_transfers', 'holder_concentration']
    X = df[feature_columns]
    y = df['risk_label']
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"训练集: {len(X_train)} 条, 测试集: {len(X_test)} 条")
    
    # 训练RandomForest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        class_weight='balanced'  # 处理类别不平衡
    )
    
    model.fit(X_train, y_train)
    
    # 评估模型
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    logger.info(f"\n{'='*50}")
    logger.info(f"🎯 模型训练完成!")
    logger.info(f"准确率: {accuracy:.2%}")
    logger.info(f"\n分类报告:\n{classification_report(y_test, y_pred)}")
    logger.info(f"{'='*50}\n")
    
    # 特征重要性
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    logger.info("📊 特征重要性:")
    for _, row in feature_importance.iterrows():
        logger.info(f"   {row['feature']}: {row['importance']:.4f}")
    
    return model, accuracy

def save_model(model, path='backend/models/risk_model.pkl'):
    """保存训练好的模型"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'wb') as f:
        pickle.dump(model, f)
    
    logger.info(f"💾 模型已保存: {path}")

def save_training_data(df, path='data/processed/training_data.csv'):
    """保存训练数据"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"💾 训练数据已保存: {path}")

def main():
    """主训练流程"""
    logger.info("🚀 Prophet Sentinel - 模型训练开始\n")
    
    # 1. 生成训练数据
    df = generate_synthetic_training_data(n_samples=2000)
    
    # 2. 保存训练数据
    save_training_data(df)
    
    # 3. 训练模型
    model, accuracy = train_risk_model(df)
    
    # 4. 保存模型
    save_model(model)
    
    # 5. 测试预测
    logger.info("\n🧪 测试预测:")
    test_cases = [
        {
            'name': '低风险协议',
            'metrics': [50000000, 0.1, 2, 0.4]
        },
        {
            'name': '中风险协议',
            'metrics': [10000000, -0.15, 5, 0.65]
        },
        {
            'name': '高风险协议',
            'metrics': [2000000, -0.35, 12, 0.88]
        }
    ]
    
    for test in test_cases:
        proba = model.predict_proba([test['metrics']])[0]
        risk_score = int(proba[1] * 100)
        logger.info(f"   {test['name']}: 风险分数 = {risk_score}")
    
    logger.info(f"\n✅ 训练完成! 准确率: {accuracy:.2%}")
    logger.info("可以运行 Flask 应用了: python backend/app.py\n")

if __name__ == '__main__':
    main()





