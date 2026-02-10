# 使用阿里云私有镜像作为基础镜像
FROM crpi-1h9mgsiii387rvos.cn-qingdao.personal.cr.aliyuncs.com/recoj/python:3.12.12-trixie

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# 设置工作目录
WORKDIR /app

# 安装系统依赖（MySQL client）
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY code/requirements.txt .

# 安装 Python 依赖
RUN pip install -r requirements.txt

# 复制项目文件
COPY code/ .

# 创建 staticfiles 目录并收集静态文件
RUN mkdir -p /app/staticfiles && python manage.py collectstatic --noinput --clear

# 暴露端口
EXPOSE 8000

# 启动应用（使用 gunicorn）
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "problemRecommend.wsgi:application"]
