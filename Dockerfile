# Prophet Sentinel API - Production Dockerfile
# Multi-stage build for optimized image size

# ==================== Builder Stage ====================
FROM python:3.11-slim as builder

LABEL maintainer="yaow1211@gmail.com"
LABEL description="Prophet Sentinel - AI Risk Guardian for DeFi"

# 设置工作目录
WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装Python依赖到独立目录
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt && \
    pip install --no-cache-dir --user gunicorn

# ==================== Runtime Stage ====================
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_ENV=production \
    FLASK_DEBUG=False \
    PORT=5001

# 创建非root用户
RUN groupadd -r prophet && useradd -r -g prophet prophet

# 设置工作目录
WORKDIR /app

# 安装运行时依赖（如需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从builder阶段复制Python包
COPY --from=builder /root/.local /home/prophet/.local

# 复制应用代码
COPY --chown=prophet:prophet backend/ ./

# 创建日志目录
RUN mkdir -p logs && chown -R prophet:prophet logs

# 切换到非root用户
USER prophet

# 更新PATH以包含用户安装的包
ENV PATH=/home/prophet/.local/bin:$PATH

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/health || exit 1

# 暴露端口
EXPOSE ${PORT}

# 启动命令
CMD ["gunicorn", \
     "--config", "gunicorn_config.py", \
     "--bind", "0.0.0.0:5001", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--timeout", "30", \
     "--graceful-timeout", "30", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app:app"]

