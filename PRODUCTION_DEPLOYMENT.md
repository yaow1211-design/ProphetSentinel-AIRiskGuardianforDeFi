# 🚀 生产环境部署指南 | Production Deployment Guide

**版本 | Version:** 2.0  
**更新日期 | Last Updated:** 2025-10-31

---

## 📋 目录 | Table of Contents

1. [改进概览](#改进概览)
2. [部署方式选择](#部署方式选择)
3. [Gunicorn 部署](#gunicorn-部署)
4. [Docker 部署](#docker-部署)
5. [Systemd 服务部署](#systemd-服务部署)
6. [性能优化](#性能优化)
7. [监控和日志](#监控和日志)
8. [安全最佳实践](#安全最佳实践)

---

## 🎯 改进概览 | Improvements Overview

### ✅ 已完成的改进

#### 1. **修复 Datetime Deprecation 警告**
```python
# 旧代码（已弃用）
timestamp = datetime.utcnow().isoformat()

# 新代码（推荐）
from datetime import datetime, UTC
timestamp = datetime.now(UTC).isoformat()
```

#### 2. **惰性初始化避免导入时副作用**
```python
# 旧代码（模块级初始化）
risk_predictor = RiskPredictor()
solana_service = SolanaService()

# 新代码（惰性初始化）
_risk_predictor: Optional[RiskPredictor] = None
_solana_service: Optional[SolanaService] = None

def get_risk_predictor() -> RiskPredictor:
    if _risk_predictor is None:
        _ensure_services_initialized()
    return _risk_predictor
```

**优势:**
- ✅ 导入时不会触发 I/O 操作
- ✅ 测试更容易（可以 mock）
- ✅ 启动更快
- ✅ 更好的资源管理

#### 3. **生产环境服务器配置**
```python
# 开发环境（不推荐生产使用）
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

# 生产环境（推荐）
gunicorn --config gunicorn_config.py app:app
```

---

## 🔀 部署方式选择 | Deployment Options

| 方式 | 优势 | 适用场景 | 难度 |
|------|------|----------|------|
| **Gunicorn + Systemd** | 简单、轻量 | Linux 服务器 | ⭐⭐ |
| **Docker** | 可移植、隔离 | 云平台、K8s | ⭐⭐⭐ |
| **PM2** | Node.js生态 | Node.js环境 | ⭐⭐ |
| **K8s** | 高可用、自动扩缩容 | 大规模部署 | ⭐⭐⭐⭐⭐ |

---

## 🦄 Gunicorn 部署 | Gunicorn Deployment

### 1. 安装依赖
```bash
cd backend
source venv/bin/activate
pip install gunicorn
```

### 2. 配置文件说明

`gunicorn_config.py` 包含完整的生产配置：

```python
# Worker配置
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
timeout = 30

# 日志配置
accesslog = '-'  # stdout
errorlog = '-'   # stderr
loglevel = 'info'

# 性能优化
max_requests = 1000  # 防止内存泄漏
max_requests_jitter = 50
keepalive = 5
```

### 3. 启动命令
```bash
# 基本启动
gunicorn --config gunicorn_config.py app:app

# 自定义参数
gunicorn \
    --config gunicorn_config.py \
    --bind 0.0.0.0:5001 \
    --workers 4 \
    --timeout 30 \
    app:app

# 后台运行
gunicorn --config gunicorn_config.py --daemon app:app
```

### 4. 环境变量
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export GUNICORN_WORKERS=4
export GUNICORN_TIMEOUT=30
```

---

## 🐳 Docker 部署 | Docker Deployment

### 1. 构建镜像
```bash
# 构建
docker build -t prophet-sentinel-api:1.0.0 .

# 查看镜像
docker images | grep prophet
```

### 2. 运行容器
```bash
# 简单运行
docker run -d \
    --name prophet-api \
    -p 5001:5001 \
    prophet-sentinel-api:1.0.0

# 带环境变量
docker run -d \
    --name prophet-api \
    -p 5001:5001 \
    -e FLASK_ENV=production \
    -e GUNICORN_WORKERS=4 \
    -v $(pwd)/logs:/app/logs \
    prophet-sentinel-api:1.0.0
```

### 3. Docker Compose（推荐）
```bash
# 启动所有服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

### 4. 多阶段构建优化

`Dockerfile` 使用多阶段构建减小镜像大小：

```dockerfile
# Builder stage - 构建依赖
FROM python:3.11-slim as builder
RUN pip install --user -r requirements.txt

# Runtime stage - 运行环境
FROM python:3.11-slim
COPY --from=builder /root/.local /home/prophet/.local
```

**镜像大小对比:**
- 单阶段构建: ~800MB
- 多阶段构建: ~250MB
- 优化比例: 68%

---

## ⚙️  Systemd 服务部署 | Systemd Deployment

### 1. 创建服务文件

将 `deployment/systemd/prophet-sentinel.service` 复制到系统目录：

```bash
sudo cp deployment/systemd/prophet-sentinel.service /etc/systemd/system/
sudo systemctl daemon-reload
```

### 2. 管理服务
```bash
# 启用（开机自启）
sudo systemctl enable prophet-sentinel

# 启动服务
sudo systemctl start prophet-sentinel

# 查看状态
sudo systemctl status prophet-sentinel

# 查看日志
sudo journalctl -u prophet-sentinel -f

# 重启服务
sudo systemctl restart prophet-sentinel

# 停止服务
sudo systemctl stop prophet-sentinel
```

### 3. 服务配置要点

```ini
[Service]
Type=notify              # 支持systemd通知机制
User=prophet             # 非root用户
Restart=always           # 自动重启
PrivateTmp=true          # 隔离临时目录
NoNewPrivileges=true     # 安全限制
LimitNOFILE=65535        # 文件描述符限制
MemoryMax=2G             # 内存限制
```

---

## 🚄 性能优化 | Performance Optimization

### 1. Worker 数量调优

```python
# CPU密集型应用
workers = (2 × CPU核心数) + 1

# I/O密集型应用
workers = (4 × CPU核心数)

# 实际配置示例（4核CPU）
workers = 9  # 2 × 4 + 1
```

### 2. Worker 类型选择

| Worker类型 | 特点 | 适用场景 |
|-----------|------|----------|
| `sync` | 同步，简单 | CPU密集型 |
| `gevent` | 异步，协程 | I/O密集型 |
| `eventlet` | 异步，绿色线程 | 高并发 |
| `tornado` | 异步，高性能 | WebSocket |

```python
# 配置示例
worker_class = 'gevent'
worker_connections = 1000
```

### 3. 连接池优化

```python
# 数据库连接池
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_MAX_OVERFLOW = 10

# Redis连接池
REDIS_MAX_CONNECTIONS = 50
```

### 4. 缓存策略

```python
# 内存缓存
from functools import lru_cache

@lru_cache(maxsize=128)
def get_protocol_metrics(protocol: str):
    # ...

# Redis缓存
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@cache.cached(timeout=300)
def expensive_operation():
    # ...
```

---

## 📊 监控和日志 | Monitoring & Logging

### 1. 日志配置

#### 应用日志
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/prophet/app.log'),
        logging.StreamHandler()
    ]
)
```

#### Gunicorn日志
```python
# gunicorn_config.py
accesslog = '/var/log/prophet/access.log'
errorlog = '/var/log/prophet/error.log'
loglevel = 'info'
```

#### 日志轮转
```bash
# /etc/logrotate.d/prophet-sentinel
/var/log/prophet/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 prophet prophet
    sharedscripts
    postrotate
        systemctl reload prophet-sentinel
    endscript
}
```

### 2. 健康检查

```bash
# HTTP健康检查
curl -f http://localhost:5001/api/health || exit 1

# 详细健康检查
{
  "status": "healthy",
  "timestamp": "2025-10-31T08:00:00+00:00",
  "model_loaded": true,
  "solana_connected": true
}
```

### 3. 监控指标

#### Prometheus集成
```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# 自定义指标
request_count = Counter('requests_total', 'Total requests')
request_latency = Histogram('request_latency_seconds', 'Request latency')
```

#### 关键指标
- **请求率**: requests/second
- **响应时间**: p50, p95, p99
- **错误率**: error/total
- **CPU使用率**: %
- **内存使用**: MB
- **Worker状态**: active/idle

---

## 🔐 安全最佳实践 | Security Best Practices

### 1. 非root用户运行
```bash
# 创建专用用户
sudo useradd -r -s /bin/false prophet

# 设置所有权
sudo chown -R prophet:prophet /opt/prophet-sentinel
```

### 2. 环境变量管理
```bash
# 使用.env文件（不要提交到Git）
echo "SECRET_KEY=your_secret_key" > .env
echo ".env" >> .gitignore

# 或使用系统环境变量
export SECRET_KEY=$(openssl rand -hex 32)
```

### 3. HTTPS配置

#### Let's Encrypt证书
```bash
# 安装certbot
sudo apt-get install certbot

# 获取证书
sudo certbot certonly --standalone -d api.prophet-sentinel.com

# 配置Nginx
ssl_certificate /etc/letsencrypt/live/domain/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/domain/privkey.pem;
```

### 4. 限流和防护

#### Nginx限流
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
    proxy_pass http://backend;
}
```

#### 应用层限流
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour", "10 per minute"]
)

@app.route('/api/predict_risk')
@limiter.limit("5 per minute")
def predict_risk():
    # ...
```

### 5. 安全头配置
```python
from flask_talisman import Talisman

Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
    }
)
```

---

## 🎯 快速部署命令 | Quick Deploy Commands

### Docker部署
```bash
git clone https://github.com/yaow1211-design/ProphetSentinel-AIRiskGuardianforDeFi.git
cd ProphetSentinel-AIRiskGuardianforDeFi
docker-compose up -d
curl http://localhost:5001/api/health
```

### Systemd部署
```bash
git clone https://github.com/yaow1211-design/ProphetSentinel-AIRiskGuardianforDeFi.git
cd ProphetSentinel-AIRiskGuardianforDeFi/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn
sudo cp ../deployment/systemd/prophet-sentinel.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start prophet-sentinel
sudo systemctl status prophet-sentinel
```

---

## 📚 相关文档 | Related Documentation

- [Docker部署详细指南](deployment/docker/README.md)
- [Systemd服务配置](deployment/systemd/README.md)
- [Gunicorn配置文件](backend/gunicorn_config.py)
- [测试指南](TESTING_GUIDE.md)

---

## ⚠️  注意事项 | Important Notes

1. **不要在生产环境使用 `app.run()`** - 这是开发服务器，性能和安全性不足
2. **务必设置环境变量 `FLASK_ENV=production`** - 关闭调试模式
3. **使用HTTPS** - 保护API通信安全
4. **配置日志轮转** - 防止日志文件过大
5. **定期备份** - 备份配置和数据
6. **监控告警** - 及时发现问题

---

## 🆘 故障排除 | Troubleshooting

### 服务启动失败
```bash
# 查看日志
sudo journalctl -u prophet-sentinel -xe

# 检查配置
gunicorn --check-config gunicorn_config.py app:app

# 测试端口
sudo netstat -tulpn | grep 5001
```

### 性能问题
```bash
# 查看资源使用
top -p $(pgrep -f gunicorn)

# 查看连接数
ss -s

# 分析慢查询
curl -w "@curl-format.txt" http://localhost:5001/api/predict_risk
```

---

**🎉 现在您的 Prophet Sentinel 已准备好用于生产环境！**

如有问题，请查看相关文档或提交 Issue。

