# 🐳 Docker 部署指南 | Docker Deployment Guide

## 📋 前置要求 | Prerequisites

- Docker >= 20.10
- Docker Compose >= 2.0
- 至少 2GB 可用内存
- 至少 5GB 可用磁盘空间

## 🚀 快速开始 | Quick Start

### 1. 克隆项目
```bash
git clone https://github.com/yaow1211-design/ProphetSentinel-AIRiskGuardianforDeFi.git
cd ProphetSentinel-AIRiskGuardianforDeFi
```

### 2. 构建镜像
```bash
# 构建镜像
docker-compose build

# 或者拉取预构建镜像（如果有）
# docker pull prophet-sentinel-api:latest
```

### 3. 启动服务
```bash
# 后台启动
docker-compose up -d

# 前台启动（查看日志）
docker-compose up
```

### 4. 验证部署
```bash
# 检查容器状态
docker-compose ps

# 测试API
curl http://localhost:5001/api/health
curl http://localhost:5001/api/predict_risk?protocol=Jupiter
```

## 🔧 配置说明 | Configuration

### 环境变量配置
创建 `.env` 文件：

```bash
# Flask配置
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5001

# Gunicorn配置
GUNICORN_WORKERS=4
GUNICORN_THREADS=1
GUNICORN_TIMEOUT=30
GUNICORN_LOG_LEVEL=info

# Solana配置（可选）
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=your_api_key_here

# 数据库配置（如需要）
# DATABASE_URL=postgresql://user:password@db:5432/prophet
```

### 自定义docker-compose.yml
```yaml
services:
  api:
    environment:
      - CUSTOM_ENV_VAR=value
    volumes:
      - ./custom/path:/app/custom
```

## 📊 管理命令 | Management Commands

### 查看日志
```bash
# 所有服务日志
docker-compose logs -f

# 只看API日志
docker-compose logs -f api

# 最近100行
docker-compose logs --tail=100 api
```

### 启动/停止/重启
```bash
# 停止所有服务
docker-compose stop

# 启动所有服务
docker-compose start

# 重启服务
docker-compose restart api

# 完全停止并删除容器
docker-compose down

# 停止并删除容器、网络、卷
docker-compose down -v
```

### 执行命令
```bash
# 进入容器
docker-compose exec api bash

# 运行命令
docker-compose exec api python -c "print('Hello')"

# 查看Python版本
docker-compose exec api python --version
```

### 扩容
```bash
# 启动3个API实例
docker-compose up -d --scale api=3

# 配置负载均衡（需要修改docker-compose.yml）
```

## 🔍 监控和调试 | Monitoring & Debugging

### 资源使用
```bash
# 查看容器资源使用
docker stats

# 查看特定容器
docker stats prophet-sentinel-api
```

### 健康检查
```bash
# 检查健康状态
docker inspect --format='{{.State.Health.Status}}' prophet-sentinel-api

# 查看健康检查日志
docker inspect prophet-sentinel-api | jq '.[0].State.Health'
```

### 调试模式
```bash
# 临时启用调试日志
docker-compose exec api \
  gunicorn --log-level debug app:app
```

## 🎯 生产环境最佳实践 | Production Best Practices

### 1. 使用具体版本标签
```yaml
services:
  api:
    image: prophet-sentinel-api:1.0.0  # 不要用 latest
```

### 2. 资源限制
```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 3. 健康检查
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5001/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### 4. 日志管理
```yaml
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 5. 使用 Secrets（敏感信息）
```yaml
services:
  api:
    secrets:
      - api_key
      - db_password

secrets:
  api_key:
    file: ./secrets/api_key.txt
  db_password:
    file: ./secrets/db_password.txt
```

## 🔐 安全配置 | Security Configuration

### 1. 非root用户运行
```dockerfile
USER prophet
```

### 2. 只读文件系统
```yaml
services:
  api:
    read_only: true
    tmpfs:
      - /tmp
      - /app/logs
```

### 3. 限制能力
```yaml
services:
  api:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### 4. 网络隔离
```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # 不能访问外网
```

## 📦 镜像优化 | Image Optimization

### 多阶段构建
```dockerfile
# Builder stage
FROM python:3.11-slim as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /home/prophet/.local
```

### 缓存优化
```bash
# 利用构建缓存
docker-compose build --pull

# 清理缓存
docker system prune -a
```

## 🚀 CI/CD 集成 | CI/CD Integration

### GitHub Actions 示例
```yaml
name: Docker Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker-compose build
      
      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push prophet-sentinel-api:latest
```

## 📈 性能调优 | Performance Tuning

### 1. Worker数量
```bash
# CPU密集型：workers = (2 × CPU核心) + 1
# I/O密集型：workers = (4 × CPU核心)
GUNICORN_WORKERS=9  # 假设4核CPU
```

### 2. 连接池
```yaml
environment:
  - DB_POOL_SIZE=20
  - DB_MAX_OVERFLOW=10
```

### 3. 缓存
```yaml
services:
  redis:
    image: redis:alpine
    command: redis-server --appendonly yes
```

## 🔄 更新部署 | Update Deployment

```bash
# 1. 拉取新代码
git pull

# 2. 重新构建镜像
docker-compose build --no-cache

# 3. 滚动更新（零停机）
docker-compose up -d --no-deps --build api

# 4. 验证
curl http://localhost:5001/api/health

# 5. 清理旧镜像
docker image prune -f
```

## ⚠️  故障排除 | Troubleshooting

### 容器无法启动
```bash
# 查看日志
docker-compose logs api

# 检查配置
docker-compose config

# 验证Dockerfile
docker build --no-cache -f Dockerfile .
```

### 网络问题
```bash
# 重建网络
docker-compose down
docker network prune
docker-compose up -d
```

### 权限问题
```bash
# 检查文件所有权
ls -la logs/

# 修复权限
sudo chown -R 1000:1000 logs/
```

## 📚 相关资源 | Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

**🎉 现在您可以使用 Docker 轻松部署 Prophet Sentinel！**

