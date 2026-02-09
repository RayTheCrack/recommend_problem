# 🔧 Docker 网络连接故障排查

## 问题描述

容器启动失败，错误信息：
```
Error response from daemon: Get "https://registry-1.docker.io/v2/": 
net/http: request canceled while waiting for connection
```

## 🔍 诊断结果

### 已完成的修复

✅ **权限问题** - 已修复
- 用户已添加到 docker 组
- sudo 无密码配置已完成

✅ **docker-compose 版本** - 已升级
- 从 docker-compose 1.29.2 升级到 docker compose v5.0.2
- 脚本已更新使用新版本

✅ **Dockerfile 版本警告** - 已修复
- 移除了所有 docker-compose 文件中的过时 `version` 字段

❌ **网络连接问题** - 系统级别
- Docker 无法访问 Docker Hub 或镜像源
- 网络连接存在严重延迟或限制

## 📋 解决方案

### 方案 A：检查网络连接（首选）

```bash
# 1. 检查 DNS
nslookup registry-1.docker.io

# 2. 测试 Docker Hub 连接
curl -I https://registry-1.docker.io/v2/

# 3. 检查防火墙
sudo ufw status

# 4. 尝试 ping
ping -c 5 registry-1.docker.io
```

### 方案 B：使用本地离线镜像

如果网络无法修复，您可以：

```bash
# 1. 在有网络的机器上构建镜像
docker build -t recommend-problem:latest .

# 2. 保存为文件
docker save recommend-problem:latest > recommend-problem.tar

# 3. 在目标机器加载
docker load < recommend-problem.tar
```

### 方案 C：配置 HTTP 代理

```bash
# 为 Docker 配置代理
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf
```

添加以下内容：
```ini
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=https://proxy.example.com:8443"
Environment="NO_PROXY=localhost,127.0.0.1"
```

然后重启：
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 方案 D：使用本地数据库

修改 `docker-compose.dev.yml`，使用本地 MySQL 而不是容器化版本：

```yaml
services:
  web:
    # ... 其他配置
    environment:
      - MYSQL_HOST=host.docker.internal  # 访问主机 MySQL
```

## 🛠️ 当前脚本状态

✅ 脚本已修复并支持：
- 自动检测 sudo 权限需求
- 使用最新的 docker compose 命令
- 完整的错误处理和日志输出
- 开发、生产两种部署模式

## 📞 建议的下一步

1. **验证网络连接**
   ```bash
   docker info
   # 查看 Registry Mirrors 配置
   ```

2. **尝试手动拉取镜像**
   ```bash
   docker pull mysql:8.0
   # 如果成功，说明网络恢复
   ```

3. **使用脚本启动**
   ```bash
   # 一旦网络恢复
   cd /home/oxythecrack/桌面/recommend_problem
   ./docker-build.sh dev up
   ```

## 💡 快速测试命令

```bash
# 检查 Docker 状态
docker version
docker ps
docker images

# 检查配置
cat /etc/docker/daemon.json

# 查看日志
journalctl -u docker.service -n 50

# 测试网络
docker run --rm busybox ping -c 3 google.com
```

## 🎯 预期结果

一旦网络连接恢复，您应该能够：

```bash
./docker-build.sh dev up
```

然后看到：
```
✓ Docker 依赖检查通过
ℹ️  将使用 docker 来运行 Docker 命令
✓ dev 环境容器启动完成

容器状态:
CONTAINER ID   IMAGE              COMMAND                  CREATED       STATUS            PORTS           NAMES
xxx            python:3.10-slim   ...                      ...           Up ...            ...             recommend_problem_web_dev
yyy            mysql:8.0          ...                      ...           Up ...            3306/tcp        recommend_problem_mysql_dev
```

然后访问：http://localhost:8000

---

**需要帮助？** 按上述方案 A 检查网络配置。

**网络恢复后？** 运行 `./docker-build.sh dev up` 启动应用。
