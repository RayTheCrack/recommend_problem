#!/bin/bash
# Django应用启动脚本

set -e

# 默认值
MYSQL_HOST=${MYSQL_HOST:-db}
MYSQL_USER=${MYSQL_USER:-root}
MYSQL_PASSWORD=${MYSQL_PASSWORD:-password}
MYSQL_PORT=${MYSQL_PORT:-3306}

echo "======================================="
echo "Django Problem Recommendation System"
echo "======================================="
echo "等待MySQL数据库就绪..."

# 等待MySQL就绪
max_tries=50
try=0
while [ $try -lt $max_tries ]; do
  if mysqladmin ping -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent 2>/dev/null; then
    echo "✓ MySQL数据库已就绪！"
    break
  fi
  try=$((try+1))
  if [ $((try % 10)) -eq 0 ]; then
    echo "  等待中... ($try/$max_tries)"
  fi
  sleep 1
done

if [ $try -eq $max_tries ]; then
  echo "✗ MySQL连接超时，请检查数据库配置"
  exit 1
fi

echo ""
echo "正在执行数据库迁移..."
python manage.py migrate --noinput || true

echo "正在收集静态文件..."
python manage.py collectstatic --noinput --clear || true

echo ""
echo "======================================="
echo "✓ 应用启动完成！"
echo "======================================="
echo "请访问应用："
if [ "$DEBUG" = "False" ]; then
  echo "  http://localhost:8000"
  echo "使用gunicorn生产服务器运行"
else
  echo "  http://localhost:8000"
  echo "使用Django开发服务器运行"
fi
echo ""

# 启动应用
exec "$@"
