# Systemd 部署指南 | Systemd Deployment Guide

## 📋 前置要求 | Prerequisites

```bash
# 创建系统用户
sudo useradd -r -s /bin/false prophet

# 创建目录
sudo mkdir -p /opt/prophet-sentinel
sudo mkdir -p /opt/prophet-sentinel/logs
sudo chown -R prophet:prophet /opt/prophet-sentinel
```

## 🚀 安装步骤 | Installation Steps

### 1. 部署代码
```bash
# 克隆或复制代码到服务器
sudo cp -r /path/to/ProphetSentinel-AIRiskGuardianforDeFi/* /opt/prophet-sentinel/

# 设置权限
sudo chown -R prophet:prophet /opt/prophet-sentinel
```

### 2. 安装依赖
```bash
cd /opt/prophet-sentinel/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 3. 安装 Systemd Service
```bash
# 复制service文件
sudo cp deployment/systemd/prophet-sentinel.service /etc/systemd/system/

# 重新加载systemd
sudo systemctl daemon-reload

# 启用服务（开机自启）
sudo systemctl enable prophet-sentinel

# 启动服务
sudo systemctl start prophet-sentinel
```

## 🔧 管理命令 | Management Commands

### 查看状态
```bash
sudo systemctl status prophet-sentinel
```

### 启动/停止/重启
```bash
sudo systemctl start prophet-sentinel
sudo systemctl stop prophet-sentinel
sudo systemctl restart prophet-sentinel
```

### 查看日志
```bash
# 实时日志
sudo journalctl -u prophet-sentinel -f

# 最近100行日志
sudo journalctl -u prophet-sentinel -n 100

# 今天的日志
sudo journalctl -u prophet-sentinel --since today
```

### 重新加载配置
```bash
sudo systemctl daemon-reload
sudo systemctl restart prophet-sentinel
```

## 🔍 故障排除 | Troubleshooting

### 服务无法启动
```bash
# 检查服务状态
sudo systemctl status prophet-sentinel

# 查看详细日志
sudo journalctl -u prophet-sentinel -xe

# 检查配置文件
sudo systemctl cat prophet-sentinel
```

### 权限问题
```bash
# 检查文件所有权
ls -la /opt/prophet-sentinel

# 修复权限
sudo chown -R prophet:prophet /opt/prophet-sentinel
sudo chmod -R 755 /opt/prophet-sentinel
```

## 🔐 Nginx 反向代理 | Nginx Reverse Proxy

```nginx
upstream prophet_sentinel {
    server 127.0.0.1:5001;
    keepalive 32;
}

server {
    listen 80;
    server_name api.prophet-sentinel.com;

    # SSL配置（推荐）
    # listen 443 ssl http2;
    # ssl_certificate /etc/letsencrypt/live/domain/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/domain/privkey.pem;

    location / {
        proxy_pass http://prophet_sentinel;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # WebSocket支持（如需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 📊 性能监控 | Performance Monitoring

### 资源使用
```bash
# CPU和内存使用
systemctl status prophet-sentinel

# 详细统计
systemd-cgtop -m
```

### 进程监控
```bash
# 查看进程
ps aux | grep gunicorn

# 查看端口
sudo netstat -tulpn | grep 5001
```

## 🔄 更新部署 | Update Deployment

```bash
# 1. 停止服务
sudo systemctl stop prophet-sentinel

# 2. 拉取新代码
cd /opt/prophet-sentinel
sudo -u prophet git pull

# 3. 更新依赖
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 4. 重启服务
sudo systemctl start prophet-sentinel

# 5. 验证
sudo systemctl status prophet-sentinel
```

## 🎯 最佳实践 | Best Practices

1. **使用专用用户**: 不要使用root运行服务
2. **配置日志轮转**: 防止日志文件过大
3. **设置监控告警**: 使用 Prometheus + Grafana
4. **定期备份**: 备份配置和数据
5. **SSL/TLS**: 使用 HTTPS 保护 API
6. **限流**: 使用 Nginx 或 API Gateway 限流
7. **健康检查**: 配置负载均衡器健康检查

