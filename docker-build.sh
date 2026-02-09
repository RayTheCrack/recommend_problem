#!/bin/bash

# Docker 快速构建和启动脚本
# 用法: ./docker-build.sh [dev|prod] [up|down|build|logs]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认值
ENV=${1:-dev}
ACTION=${2:-up}

# 函数：打印带颜色的输出
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 检查是否需要 sudo
check_sudo() {
    # 使用新版 Docker Compose (docker compose) 而不是旧版 (docker-compose)
    DOCKER_CMD="docker compose"
    
    # 如果用户不能直接运行 docker，添加 sudo
    if ! docker ps &> /dev/null; then
        DOCKER_CMD="sudo docker compose"
        echo "ℹ️  将使用 sudo 来运行 Docker 命令"
    fi
}

# 函数：显示帮助信息
show_help() {
    cat << EOF
Docker 容器化管理脚本

用法: ./docker-build.sh [环境] [操作]

环境选项:
  dev     开发环境 (默认)
  prod    生产环境

操作选项:
  up      启动容器 (默认)
  down    停止容器
  build   重建镜像
  logs    查看日志
  ps      查看容器状态
  shell   进入Django容器shell
  clean   清理所有容器和镜像

示例:
  ./docker-build.sh dev up     # 启动开发环境
  ./docker-build.sh prod build # 构建生产镜像
  ./docker-build.sh dev logs   # 查看开发环境日志
EOF
}

# 检查 docker 和 docker-compose
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    # 检查新版 Docker Compose 插件或旧版 docker-compose
    if ! docker compose version &> /dev/null && ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    print_success "Docker 依赖检查通过"
}

# 选择正确的 compose 文件
get_compose_file() {
    if [ "$ENV" = "dev" ]; then
        echo "docker-compose.dev.yml"
    else
        echo "docker-compose.yml"
    fi
}

# 启动容器
start_containers() {
    COMPOSE_FILE=$(get_compose_file)
    print_info "正在启动 $ENV 环境容器（使用 $COMPOSE_FILE）..."
    $DOCKER_CMD -f "$COMPOSE_FILE" up -d
    print_success "$ENV 环境容器启动完成"
    
    # 显示容器状态
    print_info "容器状态:"
    $DOCKER_CMD -f "$COMPOSE_FILE" ps
}

# 停止容器
stop_containers() {
    COMPOSE_FILE=$(get_compose_file)
    print_info "正在停止 $ENV 环境容器..."
    $DOCKER_CMD -f "$COMPOSE_FILE" down
    print_success "$ENV 环境容器已停止"
}

# 构建镜像
build_images() {
    COMPOSE_FILE=$(get_compose_file)
    print_info "正在构建 $ENV 环境镜像..."
    $DOCKER_CMD -f "$COMPOSE_FILE" build --no-cache
    print_success "$ENV 环境镜像构建完成"
}

# 查看日志
show_logs() {
    COMPOSE_FILE=$(get_compose_file)
    print_info "正在显示 $ENV 环境日志（按 Ctrl+C 退出）..."
    $DOCKER_CMD -f "$COMPOSE_FILE" logs -f
}

# 查看容器状态
show_ps() {
    COMPOSE_FILE=$(get_compose_file)
    print_info "$ENV 环境容器状态:"
    $DOCKER_CMD -f "$COMPOSE_FILE" ps
}

# 进入 Django shell
enter_shell() {
    COMPOSE_FILE=$(get_compose_file)
    print_info "进入 $ENV 环境 Django 容器..."
    $DOCKER_CMD -f "$COMPOSE_FILE" exec web python manage.py shell
}

# 清理容器和镜像
clean_all() {
    print_warning "即将删除所有 Docker 容器、镜像和数据卷，此操作不可撤销！"
    read -p "确认删除? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "正在清理..."
        $DOCKER_CMD -f "docker-compose.dev.yml" down -v 2>/dev/null || true
        $DOCKER_CMD -f "docker-compose.yml" down -v 2>/dev/null || true
        sudo docker system prune -a --volumes -f
        print_success "清理完成"
    else
        print_info "已取消"
    fi
}

# 主逻辑
main() {
    # 检查参数
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_help
        exit 0
    fi
    
    # 检查依赖和 sudo
    check_dependencies
    check_sudo
    
    print_info "环境: $ENV, 操作: $ACTION"
    print_info "Docker 命令: $DOCKER_CMD"
    
    case $ACTION in
        up)
            start_containers
            ;;
        down)
            stop_containers
            ;;
        build)
            build_images
            ;;
        logs)
            show_logs
            ;;
        ps)
            show_ps
            ;;
        shell)
            enter_shell
            ;;
        clean)
            clean_all
            ;;
        *)
            print_error "未知操作: $ACTION"
            show_help
            exit 1
            ;;
    esac
}

# 调用主函数
main "$@"
