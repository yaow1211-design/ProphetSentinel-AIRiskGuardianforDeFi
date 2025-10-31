"""
Gunicorn 生产环境配置
Prophet Sentinel API Server Configuration
"""
import multiprocessing
import os

# ==================== Server Socket ====================
bind = f"0.0.0.0:{os.getenv('PORT', '5001')}"
backlog = 2048

# ==================== Worker Processes ====================
# 推荐的 workers 数量: (2 x CPU核心数) + 1
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'  # 可选: 'sync', 'gevent', 'eventlet'
worker_connections = 1000
max_requests = 1000  # 防止内存泄漏，每处理1000个请求后重启worker
max_requests_jitter = 50  # 添加随机抖动，避免所有worker同时重启
timeout = 30  # 请求超时时间（秒）
keepalive = 5  # Keep-Alive连接时间（秒）

# ==================== Threading ====================
threads = int(os.getenv('GUNICORN_THREADS', 1))

# ==================== Server Mechanics ====================
daemon = False  # 不作为守护进程运行（systemd会管理）
pidfile = None  # systemd不需要pidfile
umask = 0
user = None
group = None
tmp_upload_dir = None

# ==================== Logging ====================
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '-')  # - 表示stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
errorlog = os.getenv('GUNICORN_ERROR_LOG', '-')  # - 表示stderr
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')  # debug, info, warning, error, critical
capture_output = False  # 不捕获stdout/stderr
enable_stdio_inheritance = False

# ==================== Process Naming ====================
proc_name = 'prophet-sentinel-api'

# ==================== Server Hooks ====================

def on_starting(server):
    """服务器启动时调用"""
    server.log.info("🚀 Prophet Sentinel API 服务器启动中...")


def on_reload(server):
    """配置重载时调用"""
    server.log.info("🔄 Prophet Sentinel API 配置重载中...")


def when_ready(server):
    """服务器准备就绪时调用"""
    server.log.info(f"✅ Prophet Sentinel API 已就绪，监听 {bind}")


def pre_fork(server, worker):
    """Fork worker进程之前调用"""
    pass


def post_fork(server, worker):
    """Fork worker进程之后调用"""
    server.log.info(f"👷 Worker {worker.pid} 已生成")


def post_worker_init(worker):
    """Worker初始化完成后调用"""
    worker.log.info(f"⚙️  Worker {worker.pid} 初始化完成")


def worker_int(worker):
    """Worker收到SIGINT或SIGQUIT信号时调用"""
    worker.log.info(f"⏸️  Worker {worker.pid} 收到中断信号")


def worker_abort(worker):
    """Worker收到SIGABRT信号时调用"""
    worker.log.info(f"💥 Worker {worker.pid} 异常中止")


def pre_exec(server):
    """执行新的二进制文件之前调用（用于代码热更新）"""
    server.log.info("🔄 准备执行新的二进制文件...")


def pre_request(worker, req):
    """处理请求之前调用"""
    worker.log.debug(f"{req.method} {req.path}")


def post_request(worker, req, environ, resp):
    """处理请求之后调用"""
    pass


def child_exit(server, worker):
    """Worker退出时调用"""
    server.log.info(f"👋 Worker {worker.pid} 已退出")


def worker_exit(server, worker):
    """Worker退出时调用（清理资源）"""
    pass


def nworkers_changed(server, new_value, old_value):
    """Worker数量改变时调用"""
    server.log.info(f"⚖️  Workers 数量从 {old_value} 变更为 {new_value}")


def on_exit(server):
    """服务器退出时调用"""
    server.log.info("👋 Prophet Sentinel API 服务器关闭")

# ==================== SSL 配置 ====================
# 如果需要 HTTPS，取消注释并配置以下选项
# keyfile = '/path/to/keyfile.key'
# certfile = '/path/to/certfile.crt'
# ssl_version = ssl.PROTOCOL_TLSv1_2
# cert_reqs = ssl.CERT_NONE
# ca_certs = None
# suppress_ragged_eofs = True
# do_handshake_on_connect = False
# ciphers = None

# ==================== Security ====================
limit_request_line = 4094  # HTTP请求行最大长度
limit_request_fields = 100  # HTTP请求头字段数量限制
limit_request_field_size = 8190  # HTTP请求头字段大小限制

# ==================== Development Settings ====================
reload = os.getenv('GUNICORN_RELOAD', 'false').lower() == 'true'  # 生产环境应设为False
reload_engine = 'auto'
reload_extra_files = []
spew = False  # 打印服务器执行的每一条语句（仅用于调试）
check_config = False

# ==================== Environment Variables ====================
# 从环境变量读取额外配置
raw_env = [
    f'FLASK_ENV={os.getenv("FLASK_ENV", "production")}',
    f'FLASK_DEBUG={os.getenv("FLASK_DEBUG", "False")}',
]

