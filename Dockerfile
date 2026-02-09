# 基础镜像（Python3.10 + 阿里云源加速）
FROM python:3.10-slim

# 维护者信息
LABEL maintainer="Gazy0906@outlook.com" \
      version="1.0" \
      description="Django Problem Recommendation System - Production Image"

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=Asia/Shanghai

# 创建非root用户（提高安全性）
RUN groupadd -r django && useradd -r -g django django

# 安装系统依赖（MySQL客户端、生产环境必需的库）
RUN apt update && apt install -y --no-install-recommends \
    default-mysql-client \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 设置时区（避免时间错误）
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 复制依赖文件并安装Python依赖（先复制requirements.txt，利用Docker缓存）
COPY code/requirements.txt /app/
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install gunicorn==21.2.0 -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目所有代码
COPY code/ /app/

# 复制启动脚本
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# 创建必要的目录
RUN mkdir -p /app/staticfiles /app/logs && \
    chown -R django:django /app

# 切换到非root用户
USER django

# 暴露端口（Django默认8000）
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# 启动命令（生产环境推荐gunicorn）
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "problemRecommend.wsgi:application", "--workers", "4", "--threads", "2", "--worker-class", "sync", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-"]
