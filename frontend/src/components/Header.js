import React from 'react';
import './Header.css';

function Header({ darkMode, setDarkMode }) {
  return (
    <header className="header">
      <div className="container header-content">
        <div className="logo">
          <span className="logo-icon">🧠</span>
          <span className="logo-text">Prophet Sentinel</span>
        </div>
        
        <nav className="nav">
          <a href="#features" className="nav-link">功能</a>
          <a href="#how-it-works" className="nav-link">原理</a>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="nav-link">
            GitHub
          </a>
          
          <button 
            className="theme-toggle"
            onClick={() => setDarkMode(!darkMode)}
            title={darkMode ? '切换到浅色模式' : '切换到深色模式'}
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </nav>
      </div>
    </header>
  );
}

export default Header;


