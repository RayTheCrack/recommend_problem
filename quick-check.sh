#!/bin/bash

# 快速诊断脚本
echo "======================================"
echo "🔍 Docker 快速诊断"
echo "======================================"
echo ""

# 1. Docker 基础检查
echo "1️⃣  检查 Docker 安装..."
if command -v docker &> /dev/null; then
    docker_version=$(docker --version 2>/dev/null | grep -oP '[\d.]+' | head -1)
    echo "   ✅ Docker 已安装 (版本: $docker_version)"
else
    echo "   ❌ Docker 未安装"
    exit 1
fi

# 2. Docker 权限检查
echo ""
echo "2️⃣  检查 Docker 权限..."
if docker ps &> /dev/null; then
    echo "   ✅ 有权限访问 Docker"
else
    echo "   ❌ 无权限 - 需要运行: sudo usermod -aG docker \$USER"
    exit 1
fi

# 3. Docker Compose 检查
echo ""
echo "3️⃣  检查 Docker Compose..."
if docker compose version &> /dev/null; then
    compose_version=$(docker compose version 2>/dev/null | grep -oP '[\d.]+' | head -1)
    echo "   ✅ Docker Compose 已安装 (版本: $compose_version)"
else
    echo "   ❌ Docker Compose 不可用"
    exit 1
fi

# 4. 网络连接检查
echo ""
echo "4️⃣  检查网络连接..."
if timeout 5 curl -s -I https://google.com &> /dev/null; then
    echo "   ✅ 网络连接正常"
else
    echo "   ❌ 网络连接有问题"
fi

# 5. Docker Hub 连接检查
echo ""
echo "5️⃣  检查 Docker Hub 连接..."
if timeout 5 curl -s -I https://registry-1.docker.io &> /dev/null; then
    echo "   ✅ Docker Hub 可访问"
else
    echo "   ⚠️  Docker Hub 无法连接"
fi

# 6. 尝试拉取最小镜像
echo ""
echo "6️⃣  测试拉取镜像..."
echo "   正在下载 busybox (大小: 1.2MB)..."
if timeout 30 docker pull busybox:latest &> /dev/null; then
    echo "   ✅ 成功拉取镜像"
else
    echo "   ❌ 无法拉取镜像 - 网络或代理问题"
fi

# 7. 检查 docker-compose 文件
echo ""
echo "7️⃣  检查配置文件..."
if [ -f "docker-compose.dev.yml" ]; then
    if docker compose -f docker-compose.dev.yml config > /dev/null 2>&1; then
        echo "   ✅ docker-compose.dev.yml 有效"
    else
        echo "   ❌ docker-compose.dev.yml 无效"
    fi
else
    echo "   ⚠️  docker-compose.dev.yml 不存在"
fi

# 8. 脚本检查
echo ""
echo "8️⃣  检查启动脚本..."
if [ -f "docker-build.sh" ] && [ -x "docker-build.sh" ]; then
    echo "   ✅ docker-build.sh 已就绪"
else
    echo "   ⚠️  docker-build.sh 需要配置权限"
    echo "      运行: chmod +x docker-build.sh"
fi

echo ""
echo "======================================"
echo "✨ 诊断完成"
echo "======================================"
echo ""
echo "如果所有检查都通过，可以运行:"
echo "  ./docker-build.sh dev up"
echo ""
