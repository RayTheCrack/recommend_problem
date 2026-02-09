from django.contrib import admin
from django.urls import path, re_path
from problem import views

urlpatterns = [
    # 接收四个参数，分别是两个必选参数：route、view 和两个可选参数：kwargs、name。
    # route: 字符串，表示 URL 规则，与之匹配的 URL 会执行对应的第二个参数 view。
    # view: 用于执行与正则表达式匹配的 URL 请求。
    # kwargs: 视图使用的字典类型的参数。
    # name: 为 URL 路由指定一个唯一的名称，以便在代码的其他地方引用它。这对于在模板中生成 URL 或在代码中进行重定向等操作非常有用
    path('admin/', admin.site.urls),  # 管理员
    re_path('^$', views.login),  # 默认访问登录页面  # re_path('^$', views.login) 与 path('', views.login) 效果一样
    path('login/', views.login, name="login"),  # 登入 # name
    path('register/', views.register, name="register"),  # 注册
    path('logout/', views.logout, name="logout"),  # 登出
    path('index/', views.index, name="index"),  # 主页
    path('welcome/', views.welcome, name="welcome"),  # 欢迎页
    path('start_spider/', views.start_spider, name="start_spider"),  # 启动爬虫接口
    path('problem_list/', views.problem_list, name="problem_list"),  # 题目列表
    re_path(r'^get_problem_list/$', views.get_problem_list, name="get_problem_list"),  # 获取题目列表
    path('get_psutil/', views.get_psutil, name="get_psutil"),  # 获取系统信息
    path('get_pie/', views.get_pie, name="get_pie"),  # 获取饼图数据
    path('send_problem/', views.send_problem, name="send_problem"),  # 提交
    path('problem_expect/', views.problem_expect, name="problem_expect"),  # 求职意向
    path('get_recommend/', views.get_recommend, name="get_recommend"),  # 题目推荐
    path('send_list/', views.send_list, name="send_list"),  # 已投递列表
    path('send_page/', views.send_page, name="send_page"),  # 已投递列表
    path('pass_page/', views.pass_page, name="pass_page"),
    path('up_info/', views.up_info, name="up_info"),  # 修改信息
    path('Heatmap/', views.Heatmap, name="Heatmap"),
    path('radar/', views.radar, name="radar"),
    path('chart/', views.chart, name="chart"),
]
