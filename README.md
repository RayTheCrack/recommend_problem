# 算法题目推荐平台

一个基于 Django + ECharts 的算法题目推荐系统，帮助用户分析 Codeforces 做题数据并推荐相关题目。

## 功能特性

- 👤 **用户认证**：登录/注册系统
- 📊 **数据可视化**：热力图、雷达图、直方图展示做题情况
- 🔍 **题目推荐**：基于用户做题记录智能推荐
- 📈 **统计分析**：详细的做题统计和分析
- 🎯 **求职意向**：支持设置技能标签和职位期望

## 快速开始

### 前置要求

- Docker & Docker Compose（或手动 Docker 命令）
- 已构建的 Docker 镜像：`rec_oj`

### 方法一：Docker Compose（推荐）

#### 1. 准备 docker-compose.yml

如果项目根目录还没有 `docker-compose.yml`，创建如下文件：

```yaml
version: '3.8'

services:
  # MySQL 数据库服务
  recommend_db:
    image: crpi-1h9mgsiii387rvos.cn-qingdao.personal.cr.aliyuncs.com/recoj/mysql:8.0
    container_name: recommend_db
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: recommend_problem
      MYSQL_USER: django
      MYSQL_PASSWORD: django123
    ports:
      - "3306:3306"
    volumes:
      - recommend_mysql_data:/var/lib/mysql
      - ./recommend_problem.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - recommend_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  # Django 应用服务
  recommend_app:
    image: rec_oj:latest
    container_name: recommend_app
    depends_on:
      recommend_db:
        condition: service_healthy
    environment:
      MYSQL_HOST: recommend_db
      MYSQL_USER: django
      MYSQL_PASSWORD: django123
      MYSQL_DATABASE: recommend_problem
      MYSQL_PORT: 3306
      DEBUG: "False"
      ALLOWED_HOSTS: "localhost,127.0.0.1,*"
    ports:
      - "8000:8000"
    volumes:
      - ./code:/app
    networks:
      - recommend_network
    command: bash -c "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 problemRecommend.wsgi:application"

volumes:
  recommend_mysql_data:

networks:
  recommend_network:
```

#### 2. 启动服务

```bash
# 切换到项目根目录
cd /path/to/recommend_problem

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f recommend_app
docker-compose logs -f recommend_db
```

#### 3. 停止服务

```bash
docker-compose down

# 同时删除数据卷
docker-compose down -v
```

---

### 方法二：手动 Docker 命令

#### 1. 启动 MySQL 容器

```bash
docker run -d \
  --name recommend_db \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=recommend_problem \
  -e MYSQL_USER=django \
  -e MYSQL_PASSWORD=django123 \
  -p 3306:3306 \
  -v recommend_mysql_data:/var/lib/mysql \
  crpi-1h9mgsiii387rvos.cn-qingdao.personal.cr.aliyuncs.com/recoj/mysql:8.0
```

#### 2. 等待 MySQL 启动完成

```bash
sleep 15
```

#### 3. 导入数据库

```bash
docker exec -i recommend_db mysql -uroot -prootpassword recommend_problem < recommend_problem.sql
```

#### 4. 启动应用容器

```bash
docker run -d \
  --name recommend_app \
  --link recommend_db:db \
  -e MYSQL_HOST=db \
  -e MYSQL_USER=django \
  -e MYSQL_PASSWORD=django123 \
  -e MYSQL_DATABASE=recommend_problem \
  -e MYSQL_PORT=3306 \
  -e DEBUG=False \
  -e ALLOWED_HOSTS='localhost,127.0.0.1,*' \
  -p 8000:8000 \
  -v "$(pwd)/code:/app" \
  rec_oj
```

#### 5. 查看应用日志

```bash
docker logs -f recommend_app
```

---

## 访问应用

启动成功后，在浏览器中访问：

- **主页**：http://localhost:8000
- **登录**：http://localhost:8000/login
- **注册**：http://localhost:8000/register
- **管理后台**：http://localhost:8000/admin

## 测试账号

以下是数据库中预置的测试账号（来自 `recommend_problem.sql`）：

| 账号 | 密码 | 用户名 |
|------|------|--------|
| OxyTheCrack | test123456 | OxyTheCrack |
| 1 | 1 | LHK_CN |
| 2 | 2 | 管理员 |
| 3 | user0001 | user0001 |
| 4 | user0002 | user0002 |
| 5 | user0003 | user0003 |
| 6 | 6 | 6 |

## 环境变量配置

启动应用容器时，可通过环境变量自定义配置：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `MYSQL_HOST` | `127.0.0.1` | MySQL 服务器主机（容器内使用 `db` 或 `recommend_db`） |
| `MYSQL_PORT` | `3306` | MySQL 服务器端口 |
| `MYSQL_USER` | `root` | MySQL 用户名 |
| `MYSQL_PASSWORD` | `password` | MySQL 密码 |
| `MYSQL_DATABASE` | `recommend_problem` | MySQL 数据库名 |
| `DEBUG` | `True` | Django 调试模式（生产环境应设为 `False`） |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Django 允许的主机列表 |

## 常见问题

### 1. 容器启动失败，提示"端口已占用"

```bash
# 查看占用 3306 或 8000 的进程 防止端口占用
sudo lsof -i :3306
sudo lsof -i :8000

# 关闭占用进程或使用其他端口映射
# 例如，将 MySQL 映射到 3307：
docker run -d -p 3307:3306 ...

# 或停止系统中的 MySQL 服务
sudo systemctl stop mysql
sudo service mysql stop
```

### 2. 页面无法加载静态文件（CSS/JS）

```bash
# 重新收集静态文件
docker exec recommend_app python manage.py collectstatic --noinput

# 重启应用容器
docker restart recommend_app
```

### 3. 登录后无法查看可视化图表（数据可视化返回 500）

确保：
- MySQL 容器正常运行且数据已导入
- 应用容器的 `MYSQL_HOST` 正确指向 MySQL 容器
- 检查应用日志：`docker logs recommend_app`

### 4. 如何重置数据库

```bash
# 删除数据卷（Docker Compose）
docker-compose down -v

# 或删除数据卷（手动 Docker）
docker volume rm recommend_mysql_data

# 重新启动服务即可重新初始化数据库
```

## 项目结构

```
recommend_problem/
├── code/
│   ├── manage.py           # Django 管理脚本
│   ├── requirements.txt    # Python 依赖
│   ├── problem/            # Django 应用
│   │   ├── models.py       # 数据模型
│   │   ├── views.py        # 视图函数
│   │   ├── sql.py          # 数据库操作
│   │   └── ...
│   ├── problemRecommend/   # Django 项目配置
│   │   ├── settings.py     # 项目设置
│   │   ├── urls.py         # URL 路由
│   │   └── wsgi.py         # WSGI 配置
│   ├── templates/          # HTML 模板
│   └── static/             # 静态资源（CSS/JS）
├── Dockerfile              # Docker 镜像构建文件
├── docker-compose.yml      # Docker Compose 配置
├── recommend_problem.sql   # 数据库初始化脚本
└── README.md               # 本文件
```

## 技术栈

- **后端**：Django 4.2.20
- **数据库**：MySQL 8.0
- **服务器**：Gunicorn
- **前端**：HTML + JavaScript + ECharts 5.4.3
- **UI 框架**：Layui Admin
- **容器化**：Docker & Docker Compose

## 部署建议

### 开发环境

```bash
docker run -d \
  -e DEBUG=True \
  -e ALLOWED_HOSTS='*' \
  -p 8000:8000 \
  ...
```

### 生产环境

```bash
docker run -d \
  -e DEBUG=False \
  -e ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com' \
  -e MYSQL_HOST=production_db_host \
  -p 80:8000 \
  ...
```

## 许可证

MIT

## 联系方式

如有问题或建议，请提交 Issue 或 PR。
