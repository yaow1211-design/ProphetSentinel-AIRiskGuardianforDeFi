/**
 * API服务模块
 * 封装所有与后端的通信
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log(`🔵 API请求: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  error => {
    console.error('❌ 请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log(`🟢 API响应: ${response.config.url}`, response.data);
    return response;
  },
  error => {
    console.error('❌ 响应错误:', error);
    return Promise.reject(error);
  }
);

/**
 * 获取协议风险预测
 * @param {string} protocol - 协议名称
 * @returns {Promise} 风险数据
 */
export const getPredictRisk = async (protocol) => {
  try {
    const response = await api.get('/api/predict_risk', {
      params: { protocol }
    });
    return response.data;
  } catch (error) {
    console.error(`获取 ${protocol} 风险失败:`, error);
    throw error;
  }
};

/**
 * 获取支持的协议列表
 * @returns {Promise} 协议列表
 */
export const getProtocols = async () => {
  try {
    const response = await api.get('/api/protocols');
    return response.data;
  } catch (error) {
    console.error('获取协议列表失败:', error);
    throw error;
  }
};

/**
 * 健康检查
 * @returns {Promise} 健康状态
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('健康检查失败:', error);
    throw error;
  }
};

/**
 * zk隐私验证
 * @param {string} walletHash - 钱包hash
 * @param {number} riskScore - 风险分数
 * @returns {Promise} 验证结果
 */
export const verifyProof = async (walletHash, riskScore) => {
  try {
    const response = await api.post('/api/verify_proof', {
      wallet_hash: walletHash,
      risk_score: riskScore
    });
    return response.data;
  } catch (error) {
    console.error('zk验证失败:', error);
    throw error;
  }
};

export default api;


