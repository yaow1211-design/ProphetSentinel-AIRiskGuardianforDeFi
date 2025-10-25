import React, { useState, useEffect } from 'react';
import './App.css';
import RiskHeatmap from './components/RiskHeatmap';
import ProtocolCard from './components/ProtocolCard';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  const [selectedProtocol, setSelectedProtocol] = useState(null);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    document.body.className = darkMode ? 'dark-mode' : 'light-mode';
  }, [darkMode]);

  return (
    <div className="App">
      <Header darkMode={darkMode} setDarkMode={setDarkMode} />
      
      <main className="main-content">
        <div className="container">
          {/* Hero Section */}
          <section className="hero">
            <h1 className="hero-title">
              🧠 Prophet Sentinel
            </h1>
            <p className="hero-subtitle">
              AI预言 + 隐私盾 + 即时警报，为DeFi用户提供链上风险防护
            </p>
            <div className="hero-stats">
              <div className="stat-item">
                <div className="stat-value">6+</div>
                <div className="stat-label">支持协议</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">&lt;2s</div>
                <div className="stat-label">响应时间</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">实时</div>
                <div className="stat-label">风险预测</div>
              </div>
            </div>
          </section>

          {/* Risk Heatmap */}
          <section className="section">
            <h2 className="section-title">🔥 实时风险热图</h2>
            <RiskHeatmap onProtocolClick={setSelectedProtocol} />
          </section>

          {/* Protocol Details */}
          {selectedProtocol && (
            <section className="section">
              <h2 className="section-title">📊 协议详情</h2>
              <ProtocolCard protocol={selectedProtocol} />
            </section>
          )}

          {/* Features */}
          <section className="section features">
            <h2 className="section-title">✨ 核心功能</h2>
            <div className="feature-grid">
              <div className="feature-card">
                <div className="feature-icon">🎯</div>
                <h3>AI风险预测</h3>
                <p>基于RandomForest模型，实时分析链上指标，输出0-100风险分数</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🤖</div>
                <h3>Telegram警报</h3>
                <p>高风险协议即时推送，支持订阅和自定义阈值</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🔒</div>
                <h3>隐私保护</h3>
                <p>zk-proof验证，分析风险时不泄露钱包地址</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🌱</div>
                <h3>绿色评分</h3>
                <p>ESG可持续性分析，推荐低能耗DeFi协议</p>
              </div>
            </div>
          </section>

          {/* How It Works */}
          <section className="section how-it-works">
            <h2 className="section-title">⚙️ 工作原理</h2>
            <div className="workflow">
              <div className="workflow-step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4>数据采集</h4>
                  <p>从Solana链上实时拉取交易量、流动性、鲸鱼活动等指标</p>
                </div>
              </div>
              
              <div className="workflow-arrow">→</div>
              
              <div className="workflow-step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4>AI分析</h4>
                  <p>ML模型处理数据，预测rug pull和闪崩概率</p>
                </div>
              </div>
              
              <div className="workflow-arrow">→</div>
              
              <div className="workflow-step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4>风险评分</h4>
                  <p>生成0-100分数和警报等级，可视化展示</p>
                </div>
              </div>
              
              <div className="workflow-arrow">→</div>
              
              <div className="workflow-step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h4>即时警报</h4>
                  <p>高风险时通过Telegram推送，帮助用户及时撤离</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;


