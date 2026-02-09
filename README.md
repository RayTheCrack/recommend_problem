# 📌 项目主README文件

> 如果您是第一次看到这个项目，请从这里开始！

## 🎯 您将看到什么

这是一个已完全容器化的 **Recommend Problem（问题推荐系统）** Django应用。

- ✅ 开发环境一键启动
- ✅ 生产环境完整配置
- ✅ 详细的中文文档
- ✅ 自动化管理脚本
- ✅ 最佳实践配置

---

## 🚀 快速开始（3步）

### 第1步：进入项目目录
```bash
cd /home/oxythecrack/桌面/recommend_problem
```

### 第2步：给脚本添加执行权限
```bash
chmod +x docker-build.sh
```

### 第3步：启动开发环境
```bash
./docker-build.sh dev up
```

**然后在浏览器中打开：** http://localhost:8000

---

## 📚 文档目录

### 🟢 新用户（必读）

**👉 [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)**
- ⏱️ 5分钟快速开始
- 🛠️ 常用命令速查
- 💻 开发工作流程

### 🟡 详细指南

**👉 [README_Docker.md](README_Docker.md)**
- 📖 完整的Docker使用指南
- 🔧 各个文件详细说明
- 💊 故障排查指南

### 🔴 生产部署

**👉 [DOCKER_PRODUCTION.md](DOCKER_PRODUCTION.md)**
- 🚀 生产环境部署步骤
- 🔐 安全最佳实践
- 📊 性能优化建议
- 🌐 Nginx反向代理配置

### 📋 项目结构

**👉 [FILE_STRUCTURE.md](FILE_STRUCTURE.md)**
- 📂 项目文件完整列表
- 🎯 文件功能说明
- 💡 使用场景指南

### ✅ 完成报告

**👉 [DOCKER_COMPLETE.md](DOCKER_COMPLETE.md)**
- 📊 完成情况统计
- ✨ 新增功能说明
- 📋 部署前检查清单

### 🎚️ 快速参考卡

**👉 [QUICK_REFERENCE.sh](QUICK_REFERENCE.sh)**
```bash
bash QUICK_REFERENCE.sh  # 显示快速参考卡
```

---

## 🎯 选择您的路径

### 我想快速开始开发 ⚡

```bash
./docker-build.sh dev up
```

然后查看 👉 [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)

### 我想部署到生产 🚀

1. 阅读 👉 [DOCKER_PRODUCTION.md](DOCKER_PRODUCTION.md)
2. 配置环境变量：`cp .env.example .env && nano .env`
3. 启动生产环境：`docker-compose up -d`

### 我想了解项目结构 📂

查看 👉 [FILE_STRUCTURE.md](FILE_STRUCTURE.md)

### 我遇到了问题 💊

查看 👉 [README_Docker.md](README_Docker.md) 的故障排查部分

---

## 💻 常用命令

```bash
# 启动开发环境
./docker-build.sh dev up

# 查看日志
./docker-build.sh dev logs

# 停止容器
./docker-build.sh dev down

# 进入Django shell
./docker-build.sh dev shell

# 查看所有命令
./docker-build.sh -h
```

---

## 🌐 访问地址

**开发环境：**
- 应用：http://localhost:8000
- MySQL：127.0.0.1:3306 (user: root, password: password)

**生产环境（不含Nginx）：**
- 应用：http://localhost:8000
- MySQL：127.0.0.1:3306

**生产环境（含Nginx）：**
- 应用：http://localhost
- MySQL：127.0.0.1:3306

---

## 📁 项目结构简览

```
recommend_problem/
├── 📄 README.md                     ← 您在这里
├── 📄 DOCKER_QUICKSTART.md          ← 5分钟快速开始 ⭐
├── 📄 README_Docker.md              ← 完整指南
├── 📄 DOCKER_PRODUCTION.md          ← 生产部署
├── 📄 FILE_STRUCTURE.md             ← 项目结构
├── 📄 DOCKER_COMPLETE.md            ← 完成报告
│
├── 🐳 Docker配置
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod-nginx.yml
│   ├── docker-build.sh              ← 管理脚本 ⭐
│   └── ...
│
└── 📁 code/                         ← Django项目
    └── ...
```

---

## ✨ 主要特性

### 开发环境

✅ 代码热加载
✅ DEBUG模式
✅ 实时日志
✅ 快速迭代

### 生产环境

✅ Gunicorn高性能服务器
✅ 自动重启和健康检查
✅ Nginx反向代理支持
✅ 数据卷持久化
✅ 日志自动轮转
✅ 非root用户运行（安全）

---

## 🔑 环境变量配置

### 快速配置

```bash
# 复制示例
cp .env.example .env

# 编辑配置（生产环境必须修改）
nano .env
```

### 关键变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `DEBUG` | 调试模式 | False（生产）/ True（开发） |
| `SECRET_KEY` | Django密钥 | 使用新的安全密钥 |
| `ALLOWED_HOSTS` | 允许的域名 | yourdomain.com |
| `MYSQL_PASSWORD` | MySQL密码 | 使用强密码 |

---

## 📊 部署选项

### 选项1：开发环境（推荐学习）

```bash
./docker-build.sh dev up
```

特点：代码热加载、实时日志、调试模式

### 选项2：生产环境基础版

```bash
docker-compose up -d
```

特点：Gunicorn、生产配置、健康检查

### 选项3：生产环境完整版（推荐）

```bash
docker-compose -f docker-compose.prod-nginx.yml up -d
```

特点：Nginx反向代理、缓存、安全头、WebSocket

---

## 🎓 学习顺序

1. **第1步：快速开始** (5分钟)
   ```bash
   ./docker-build.sh dev up
   # 访问 http://localhost:8000
   ```
   然后查看 [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)

2. **第2步：了解项目** (10分钟)
   查看 [FILE_STRUCTURE.md](FILE_STRUCTURE.md)

3. **第3步：学习详细内容** (30分钟)
   查看 [README_Docker.md](README_Docker.md)

4. **第4步：准备生产部署** (学习时间)
   查看 [DOCKER_PRODUCTION.md](DOCKER_PRODUCTION.md)

---

## 💡 常见问题

### Q: 如何启动应用？
A: 运行 `./docker-build.sh dev up` 然后访问 http://localhost:8000

### Q: 如何查看日志？
A: 运行 `./docker-build.sh dev logs`

### Q: 如何进入容器？
A: 运行 `docker-compose exec web bash`

### Q: 如何停止应用？
A: 运行 `./docker-build.sh dev down`

### Q: 生产环境需要修改什么？
A: 查看 [DOCKER_PRODUCTION.md](DOCKER_PRODUCTION.md) 的生产部署检查清单

### Q: 如何导出数据库？
A: 运行 `docker-compose exec db mysqldump -uroot -ppassword recommend_problem > backup.sql`

---

## 🔒 安全提示

⚠️ **生产环境部署前必须修改：**

1. `SECRET_KEY` - 生成新的密钥
2. `MYSQL_PASSWORD` - 修改MySQL密码
3. `ALLOWED_HOSTS` - 设置正确的域名
4. `DEBUG` - 设置为 False

详见 [DOCKER_PRODUCTION.md](DOCKER_PRODUCTION.md)

---

## 📞 获取帮助

### 第1步：查看快速开始
👉 [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) - 5分钟入门

### 第2步：查看详细文档
👉 [README_Docker.md](README_Docker.md) - 完整参考

### 第3步：查看生产指南
👉 [DOCKER_PRODUCTION.md](DOCKER_PRODUCTION.md) - 上线指南

### 第4步：显示快速参考卡
```bash
bash QUICK_REFERENCE.sh
```

---

## 🚀 立即开始

只需三条命令：

```bash
# 1. 进入项目目录
cd /home/oxythecrack/桌面/recommend_problem

# 2. 给脚本添加执行权限
chmod +x docker-build.sh

# 3. 启动开发环境
./docker-build.sh dev up
```

然后访问 http://localhost:8000

---

## 📊 项目信息

```
项目名称：Recommend Problem（问题推荐系统）
类型：Django Web应用
Python版本：3.10
Django版本：4.2.20
数据库：MySQL 8.0
服务器：Gunicorn / Django开发服务器
代理服务器：Nginx（可选）
```

---

## 📝 相关文档

- 本项目README - 👈 您在这里
- [快速开始指南](DOCKER_QUICKSTART.md) - 5分钟上手
- [完整使用指南](README_Docker.md) - 详细参考
- [生产部署指南](DOCKER_PRODUCTION.md) - 上线指南
- [项目结构说明](FILE_STRUCTURE.md) - 文件组织
- [完成报告](DOCKER_COMPLETE.md) - 项目统计

---

## 🎉 您已准备好

✅ Docker容器化配置完成
✅ 开发环境已就绪
✅ 生产环境已配置
✅ 文档已完善
✅ 自动化脚本已准备

**现在就开始吧！** 🚀

```bash
./docker-build.sh dev up
```

---

**需要帮助？** 查看 [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) ← 强烈推荐！

**想深入了解？** 查看 [README_Docker.md](README_Docker.md)

**准备上线？** 查看 [DOCKER_PRODUCTION.md](DOCKER_PRODUCTION.md)
