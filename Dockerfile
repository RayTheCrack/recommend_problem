# 基础镜像（Python3.10 + 阿里云源加速）
FROM python:3.10-slim

# 维护者信息
LABEL maintainer="Gazy0906@outlook.com"

# 设置工作目录
WORKDIR /app

# 安装系统依赖（MySQL客户端、Chrome依赖、时区等）
RUN apt update && apt install -y \
    default-mysql-client \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# 设置时区（避免时间错误）
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 复制依赖文件并安装Python依赖（先复制requirements.txt，利用Docker缓存）
COPY code/requirements.txt /app/
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目所有代码
COPY code/ /app/

# 收集静态文件（Django生产环境必需）
RUN python manage.py collectstatic --noinput

# 暴露端口（Django默认8000）
EXPOSE 8000

# 启动命令（生产环境推荐gunicorn，开发环境用runserver）
# 生产环境（推荐）
CMD ["gunicorn", "--bind", "127.0.0.1:8000", "problemRecommend.wsgi:application", "--workers", "4"]
# 开发环境（调试用，注释上面CMD，启用下面）
# CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]