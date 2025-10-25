import React from 'react';
import './Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="container footer-content">
        <div className="footer-section">
          <h4>🧠 Prophet Sentinel</h4>
          <p>AI驱动的DeFi风险预测系统</p>
        </div>
        
        <div className="footer-section">
          <h4>快速链接</h4>
          <ul>
            <li><a href="#features">核心功能</a></li>
            <li><a href="#how-it-works">工作原理</a></li>
            <li><a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>技术栈</h4>
          <ul>
            <li>Python + Flask</li>
            <li>React + Recharts</li>
            <li>Solana Web3.js</li>
            <li>Telegram Bot API</li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>联系方式</h4>
          <ul>
            <li>📧 Email: contact@example.com</li>
            <li>🐦 Twitter: @ProphetSentinel</li>
            <li>💬 Telegram: @ProphetSentinelBot</li>
          </ul>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>© {currentYear} Prophet Sentinel. MIT License. Built with ❤️ for DeFi safety.</p>
      </div>
    </footer>
  );
}

export default Footer;


