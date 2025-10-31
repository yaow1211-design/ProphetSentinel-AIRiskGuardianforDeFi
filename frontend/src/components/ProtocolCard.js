import React, { useState, useEffect } from 'react';
import { getPredictRisk } from '../services/api';
import './ProtocolCard.css';

function ProtocolCard({ protocol }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await getPredictRisk(protocol);
        setData(result);
      } catch (error) {
        console.error('获取协议数据失败:', error);
      }
      setLoading(false);
    };

    fetchData();
  }, [protocol]);

  if (loading) {
    return (
      <div className="protocol-card">
        <div className="loading-small">加载中...</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="protocol-card">
        <div className="error-small">加载失败</div>
      </div>
    );
  }

  const getRiskColor = (score) => {
    if (score < 30) return '#22c55e';
    if (score < 70) return '#eab308';
    return '#ef4444';
  };

  return (
    <div className="protocol-card">
      <div className="protocol-card-header">
        <h3>{data.protocol}</h3>
        <span className="protocol-badge" style={{ background: getRiskColor(data.risk_score) }}>
          {data.alert_emoji} {data.alert_level.toUpperCase()}
        </span>
      </div>

      <div className="score-display">
        <div className="main-score">
          <div className="score-value" style={{ color: getRiskColor(data.risk_score) }}>
            {data.risk_score}
          </div>
          <div className="score-label">风险分数</div>
        </div>
        
        <div className="secondary-score">
          <div className="score-value" style={{ color: '#22c55e' }}>
            {data.sustainable_score}
          </div>
          <div className="score-label">绿色评分</div>
        </div>
      </div>

      <div className="metrics-grid">
        <div className="metric-item">
          <div className="metric-label">24h交易量</div>
          <div className="metric-value">
            ${(data.metrics.volume_24h / 1000000).toFixed(2)}M
          </div>
        </div>

        <div className="metric-item">
          <div className="metric-label">流动性变化</div>
          <div className="metric-value" style={{ 
            color: data.metrics.liquidity_change >= 0 ? '#22c55e' : '#ef4444' 
          }}>
            {(data.metrics.liquidity_change * 100).toFixed(1)}%
          </div>
        </div>

        <div className="metric-item">
          <div className="metric-label">鲸鱼转移</div>
          <div className="metric-value">
            {data.metrics.whale_transfers} 次
          </div>
        </div>

        <div className="metric-item">
          <div className="metric-label">持有集中度</div>
          <div className="metric-value">
            {(data.metrics.holder_concentration * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      <div className="recommendation">
        {data.risk_score < 30 && (
          <div className="rec-box rec-safe">
            ✅ <strong>安全协议</strong> - 当前指标正常，可以放心使用
          </div>
        )}
        {data.risk_score >= 30 && data.risk_score < 70 && (
          <div className="rec-box rec-caution">
            ⚠️ <strong>谨慎使用</strong> - 存在一定风险，建议分散投资
          </div>
        )}
        {data.risk_score >= 70 && (
          <div className="rec-box rec-danger">
            🚨 <strong>高风险警告</strong> - 建议立即检查持仓并考虑撤离
          </div>
        )}
      </div>

      <div className="card-footer">
        <span className="timestamp">
          更新于: {new Date(data.timestamp).toLocaleString('zh-CN')}
        </span>
        <span className="confidence">
          置信度: {(data.confidence * 100).toFixed(0)}%
        </span>
      </div>
    </div>
  );
}

export default ProtocolCard;








