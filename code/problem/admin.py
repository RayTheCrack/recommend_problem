from django.contrib import admin

# Register your models here.
from django.contrib import  admin
from .models import *

# 后台管理系统流程
# 1. 创建模型类
# 2. 注册模型类
# 3. 创建超级用户 （账号和密码） python manage.py createsuperuser  # 会提示输入用户名、邮箱、密码  会在数据库表auth_user中生成一条记录
# 4. 根路由url.py添加 path('admin/', admin.site.urls)
# 5. 启动服务器 python manage.py runserver
# 6. 访问后台管理系统 http://127.0.0.1:8000/admin


admin.site.register(ProblemData)
admin.site.register(SendList)
admin.site.register(UserExpect)
admin.site.register(UserList)

