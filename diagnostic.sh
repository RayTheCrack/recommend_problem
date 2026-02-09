#!/bin/bash

# Docker 诊断脚本
# 使用方法: chmod +x diagnostic.sh && ./diagnostic.sh

set -e

echo "======================================"
echo "🔍 Docker 诊断工具"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
PASS=0
FAIL=0
WARN=0

# 检查函数
check_command() {
    local name=$1
    local cmd=$2
    
    echo -n "检查 $name... "
    if command -v $cmd &> /dev/null; then
        echo -e "${GREEN}✓ 已安装${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ 未安装${NC}"
        ((FAIL++))
        return 1
    fi
}

# 检查docker版本
check_version() {
    local name=$1
    local cmd=$2
    local min_version=$3
    
    echo -n "检查 $name 版本... "
    local version=$($cmd --version 2>/dev/null | grep -oP '[\d.]+' | head -1)
    if [ -n "$version" ]; then
        echo -e "${GREEN}✓ $version${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ 无法获取版本${NC}"
        ((FAIL++))
        return 1
    fi
}

# 检查权限
check_docker_access() {
    echo -n "检查 Docker 权限... "
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✓ 有权限${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ 无权限${NC}"
        ((FAIL++))
        return 1
    fi
}

# 检查网络连接
check_network() {
    local host=$1
    local name=$2
    
    echo -n "检查 $name 连接... "
    if timeout 5 curl -s -I "https://$host" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 连通${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ 无法连接${NC}"
        ((FAIL++))
        return 1
    fi
}

# 尝试拉取镜像
check_docker_pull() {
    echo -n "测试 Docker 拉取镜像... "
    if timeout 30 docker pull busybox:latest &> /dev/null; then
        echo -e "${GREEN}✓ 成功${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ 失败（网络问题）${NC}"
        ((FAIL++))
        return 1
    fi
}

# 检查 docker-compose 文件
check_compose_files() {
    echo ""
    echo "检查 docker-compose 文件..."
    
    local files=(
        "docker-compose.dev.yml"
        "docker-compose.yml"
        "docker-compose.prod-nginx.yml"
    )
    
    for file in "${files[@]}"; do
        echo -n "  检查 $file... "
        if [ -f "$file" ]; then
            if docker compose -f "$file" config > /dev/null 2>&1; then
                echo -e "${GREEN}✓ 有效${NC}"
                ((PASS++))
            else
                echo -e "${RED}✗ 无效${NC}"
                ((FAIL++))
            fi
        else
            echo -e "${YELLOW}⚠ 不存在${NC}"
            ((WARN++))
        fi
    done
}

# 显示诊断摘要
show_summary() {
    echo ""
    echo "======================================"
    echo "📊 诊断结果摘要"
    echo "======================================"
    echo -e "${GREEN}✓ 通过: $PASS${NC}"
    echo -e "${RED}✗ 失败: $FAIL${NC}"
    echo -e "${YELLOW}⚠ 警告: $WARN${NC}"
    echo ""
    
    if [ $FAIL -eq 0 ]; then
        echo -e "${GREEN}✨ 一切正常！可以启动 Docker 容器${NC}"
        echo ""
        echo "运行命令:"
        echo "  ./docker-build.sh dev up"
    else
        echo -e "${RED}⚠️  发现 $FAIL 个问题需要修复${NC}"
        echo ""
        echo "查看详细信息："
        echo "  cat NETWORK_TROUBLESHOOTING.md"
    fi
    echo ""
}

# 主诊断流程
echo "🔧 基础检查"
echo "======================================"
check_command "Docker" "docker"
check_command "curl" "curl"
echo ""

echo "📦 版本检查"
echo "======================================"
check_version "Docker" "docker" "20.0"
check_version "Docker Compose" "docker compose" "2.0"
echo ""

echo "🔐 权限检查"
echo "======================================"
check_docker_access
echo ""

echo "🌐 网络连接检查"
echo "======================================"
check_network "google.com" "Google"
check_network "registry-1.docker.io" "Docker Hub"
check_network "hub-mirror.c.163.com" "网易镜像"
echo ""

echo "🐳 Docker 功能检查"
echo "======================================"
check_compose_files
echo ""

echo "📥 镜像拉取测试"
echo "======================================"
check_docker_pull
echo ""

# 显示摘要
show_summary

# 获取更多信息的提示
if [ $FAIL -gt 0 ]; then
    echo "获取更多帮助:"
    echo "  - 查看日志: sudo journalctl -u docker -n 50"
    echo "  - 检查配置: cat /etc/docker/daemon.json"
    echo "  - 详细指南: cat NETWORK_TROUBLESHOOTING.md"
fi

exit $FAIL
