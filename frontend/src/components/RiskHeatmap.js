import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer } from 'recharts';
import { getPredictRisk } from '../services/api';
import './RiskHeatmap.css';

function RiskHeatmap({ onProtocolClick }) {
  const [protocols, setProtocols] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  const PROTOCOLS = ['Jupiter', 'Orca', 'Raydium', 'Serum', 'Marinade', 'Solend'];

  const fetchAllRisks = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await Promise.all(
        PROTOCOLS.map(async (protocol) => {
          try {
            const data = await getPredictRisk(protocol);
            return {
              name: protocol,
              risk_score: data.risk_score,
              sustainable_score: data.sustainable_score,
              alert_level: data.alert_level,
              metrics: data.metrics
            };
          } catch (err) {
            console.error(`获取 ${protocol} 数据失败:`, err);
            return {
              name: protocol,
              risk_score: 0,
              sustainable_score: 0,
              alert_level: 'unknown',
              error: true
            };
          }
        })
      );
      
      setProtocols(results);
      setLastUpdate(new Date());
      setLoading(false);
    } catch (err) {
      setError('加载数据失败，请检查后端服务是否启动');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllRisks();
    
    // 每30秒自动刷新
    const interval = setInterval(fetchAllRisks, 30000);
    return () => clearInterval(interval);
  }, []);

  const getColor = (score) => {
    if (score < 30) return '#22c55e'; // 绿色
    if (score < 70) return '#eab308'; // 黄色
    return '#ef4444'; // 红色
  };

  const getRiskLabel = (score) => {
    if (score < 30) return '低风险';
    if (score < 70) return '中风险';
    return '高风险';
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="custom-tooltip">
          <h4>{data.name}</h4>
          <p><strong>风险分数:</strong> {data.risk_score}/100</p>
          <p><strong>等级:</strong> {getRiskLabel(data.risk_score)}</p>
          <p><strong>绿色评分:</strong> {data.sustainable_score}/100</p>
        </div>
      );
    }
    return null;
  };

  if (loading && protocols.length === 0) {
    return (
      <div className="heatmap-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>正在加载风险数据...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="heatmap-container">
        <div className="error">
          <p>❌ {error}</p>
          <button onClick={fetchAllRisks} className="retry-button">
            重试
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="heatmap-container">
      <div className="heatmap-header">
        <div className="update-info">
          {lastUpdate && (
            <span>
              最后更新: {lastUpdate.toLocaleTimeString('zh-CN')}
            </span>
          )}
        </div>
        <button onClick={fetchAllRisks} className="refresh-button" disabled={loading}>
          {loading ? '刷新中...' : '🔄 刷新'}
        </button>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={protocols} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis 
            dataKey="name" 
            stroke="#fff"
            style={{ fontSize: '14px' }}
          />
          <YAxis 
            domain={[0, 100]} 
            stroke="#fff"
            style={{ fontSize: '14px' }}
            label={{ value: '风险分数', angle: -90, position: 'insideLeft', fill: '#fff' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar 
            dataKey="risk_score" 
            radius={[10, 10, 0, 0]}
            onClick={(data) => onProtocolClick && onProtocolClick(data.name)}
            style={{ cursor: 'pointer' }}
          >
            {protocols.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.risk_score)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div className="risk-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ background: '#22c55e' }}></span>
          <span>低风险 (0-30)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ background: '#eab308' }}></span>
          <span>中风险 (30-70)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ background: '#ef4444' }}></span>
          <span>高风险 (70-100)</span>
        </div>
      </div>

      <div className="protocol-cards">
        {protocols.map((protocol) => (
          <div 
            key={protocol.name}
            className="mini-protocol-card"
            onClick={() => onProtocolClick && onProtocolClick(protocol.name)}
          >
            <div className="protocol-name">{protocol.name}</div>
            <div 
              className="protocol-score"
              style={{ color: getColor(protocol.risk_score) }}
            >
              {protocol.risk_score}
            </div>
            <div className="protocol-label">{getRiskLabel(protocol.risk_score)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RiskHeatmap;


