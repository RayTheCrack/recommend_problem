import json
from urllib.request import Request, urlopen
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import F
from psutil import *
from numpy import *
from django.db import transaction
from collections import defaultdict

from problem import models
from problem import problem_recommend,problem_recomm,sql
import operator

def login(request):
    if request.method == "POST":
        user = request.POST.get('user')
        pass_word = request.POST.get('password')
        print('user------>', user)
        users_list = list(
            models.UserList.objects.all().values("user_id"))
        users_id = [x['user_id'] for x in users_list]
        print(users_id)
        ret = models.UserList.objects.filter(user_id=user, pass_word=pass_word)  # 查询数据库中是否有此用户  有则返回True 无则返回False
        if user not in users_id:  # 判断用户是否存在
            return JsonResponse({'code': 1, 'msg': '该账号不存在！'})
        elif ret:
            request.session['user_id'] = user  # 设置缓存
            user_obj = ret.last()  # 获取最后一个对象 也就是最新的对象
            user_name = user_obj.user_name  # 获取用户名
            request.session['user_name'] = user_name  # 设置缓存
            return JsonResponse({'code': 0, 'msg': '登录成功！'})
        else:
            return JsonResponse({'code': 1, 'msg': '密码错误！'})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        user = request.POST.get('user')
        pass_word = request.POST.get('password')
        user_name = request.POST.get('user_name')
        users_list = list(models.UserList.objects.all().values("user_id"))
        users_id = [x['user_id'] for x in users_list]
        if user in users_id:
            return JsonResponse({'code': 1, 'msg': '该账号已存在！'})
        else:
            models.UserList.objects.create(user_id=user, user_name=user_name, pass_word=pass_word)
            request.session['user_id'] = user  # 设置缓存
            request.session['user_name'] = user_name
            return JsonResponse({'code': 0, 'msg': '注册成功！'})
    else:
        return render(request, "register.html")


def logout(request):
    request.session.flush()
    return redirect('login')


def index(request):
    """此函数用于返回主页，主页包括头部，左侧菜单"""
    return render(request, "index.html")


def welcome(request):
    """此函数用于处理控制台页面"""
    problem_data = models.ProblemData.objects.all().values()
    all_problem = len(problem_data)
    spider_info = models.SpiderInfo.objects.filter(spider_id=1).first()
    return render(request, "welcome.html", locals())


def get_user_rating(username):
    req = Request(
        url=f'https://codeforces.com/api/user.rating?handle={username}',
    )
    context = json.loads(urlopen(req).read().decode('utf-8'))
    results = context["result"]
    # 获取最后一行并提取newRating
    if results:  # 确保数组非空
        last_entry = results[-1]
        rating = last_entry["newRating"]
    else:
        rating = 1500
    # print(rating)
    return rating

def start_spider(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        username = request.session.get("user_name")
        try:
            req = Request(
                url=f'https://codeforces.com/api/user.status?handle={username}',
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            context = json.loads(urlopen(req).read().decode('utf-8'))
            problem_stats = defaultdict(lambda: {'submissions': 0, 'ac': 0})
            for submission in context['result']:
                contestId = submission['problem']['contestId']
                index = submission['problem']['index']
                problem_id = f"{contestId}{index}"
                verdict = submission['verdict']
                problem_stats[problem_id]['submissions'] += 1
                if verdict == 'OK':
                    problem_stats[problem_id]['ac'] += 1

            with transaction.atomic():
                for problem_id, stats in problem_stats.items():
                    if models.ProblemData.objects.filter(ID=problem_id).exists():
                        models.SendList.objects.update_or_create(
                            user_id=user_id,
                            problem_id=problem_id,
                            defaults={
                                'submission_count': stats['submissions'],
                                'ac_count': stats['ac']
                            }
                        )
            # 获取用户rating
            rating = get_user_rating(username)
            models.UserList.objects.filter(user_id=user_id).update(rating=rating)
            models.SpiderInfo.objects.filter(spider_id=1).update(count=F('count')+1)
            return JsonResponse({"msg": "爬取完成", "status": "success"})

        except Exception as e:
            return JsonResponse({"msg": f"爬取失败: {str(e)}", "status": "error"})

    return JsonResponse({"msg": "请求方式错误", "status": "error"})
def problem_list(request):
    return render(request, "problem_list.html", locals())


def get_problem_list(request):
    # 获取页码，确保返回的是整数默认为1
    page = request.GET.get("page", "1")
    page = int(page) if page.isdigit() else 1  # 如果是有效的数字字符串，则转为整数，否则使用默认值 1

    # 获取每页数量，确保返回的是整数默认为10
    limit = request.GET.get("limit", "15")
    limit = int(limit) if limit.isdigit() else 15  # 如果是有效的数字字符串，则转为整数，否则使用默认值 10

    rating_min = request.GET.get("rating_min", "")
    rating_max = request.GET.get("rating_max", "")
    tag = request.GET.get("tag", "")
    problem_data_list = models.ProblemData.objects.all()
    filtered_problems = problem_data_list
    if rating_min or rating_max:
        filtered_problems = filtered_problems.filter(
            Rating__gte=rating_min if rating_min else None,
            Rating__lte=rating_max if rating_max else None
        )
    if tag:
        tag_list = tag.split(",")  # 假设 tag 是逗号分隔的标签字符串
        filtered_problems = filtered_problems.filter(
            Tags__icontains=tag  # 根据 Tags 进行筛选
        )

    # 分页处理
    paginator = Paginator(filtered_problems, limit)
    problem_page = paginator.get_page(page)
    problem_data_page = list(problem_page.object_list.values('ID', 'Title', 'Tags', 'Rating', 'Solved'))  # .values() 直接转换为字典列表
    user_id = request.session.get("user_id")
    sent_problem_ids = models.SendList.objects.filter(user_id=user_id).values_list("problem_id", flat=True)
    for problem in problem_data_page:
        problem['send_key'] = 1 if problem['ID'] in sent_problem_ids else 0
    if not problem_data_page:
        return JsonResponse(
            {"code": 1, "msg": "没找到需要查询的数据！", "count": 0, "data": []}
        )

    return JsonResponse({
        "code": 0,
        "msg": "success",
        "count": paginator.count,
        "data": problem_data_page
    })


def get_psutil(request):
    """此函数用于读取cpu使用率和内存占用率"""
    return JsonResponse({'cpu_data': cpu_percent(interval=1), 'memory_data': virtual_memory()[2]})


def get_pie(request):
    # 获取所有的标签，并计算每个标签出现的次数
    tag_data = []
    problem_data = models.ProblemData.objects.all()  # 查询所有的标签数据
    tag_count = {}

    # 统计每个标签的出现次数
    for problem in problem_data:
        tags = problem.Tags.split(',')  # tags是以逗号分隔的字符串
        for tag in tags:
            tag = tag.strip()  # 去除标签两端的空格
            if tag:  # 只处理非空的标签
                if tag in tag_count:
                    tag_count[tag] += 1
                else:
                    tag_count[tag] = 1

    for tag, count in tag_count.items():
        tag_data.append({'name': tag, 'value': count})

    # 生成难度（rating）分布
    rating_data = {'0-1000': 0, '1001-1500': 0, '1501-2000': 0, '2001-2500': 0, '2500-3000+': 0}
    for problem in problem_data:
        try:
            rating = int(problem.Rating)
            # print(rating)
            if rating <= 1000:
                rating_data['0-1000'] += 1
            elif 1500 >= rating > 1001:
                rating_data['1001-1500'] += 1
            elif 2000 >= rating > 1500:
                rating_data['1501-2000'] += 1
            elif 2500 >= rating > 2000:
                rating_data['2001-2500'] += 1
            elif rating > 2500:
                rating_data['2500-3000+'] += 1
        except Exception as e:
            pass  # 处理异常

    rating_data_list = [{'name': key, 'value': value} for key, value in rating_data.items()]

    # 返回JSON响应，包含标签数据和难度分布数据
    return JsonResponse({'tag_data': tag_data, 'rating_data': rating_data_list})


def send_problem(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        problem_id = request.POST.get("problem_id")
        send_key = request.POST.get("send_key")
        # print(problem_id)
        if int(send_key) == 1:
            models.SendList.objects.filter(user_id=user_id, problem_id=problem_id).delete()
        else:
            models.SendList.objects.create(user_id=user_id, problem_id=problem_id)
        return JsonResponse({"Code": 0, "msg": "操作成功"})

def problem_expect(request):
    if request.method == "POST":
        tag = request.POST.get("tag")
        if tag == "None":
            tag = None
        user_id = request.session.get("user_id")
        user = models.UserList.objects.get(user_id=user_id)
        ret = models.UserExpect.objects.filter(user=user)
        if ret.exists():
            ret.update(tag=tag)
        else:
            models.UserExpect.objects.create(user=user, tag=tag)
        return JsonResponse({"Code": 0, "msg": "操作成功"})
    else:
        ret = models.UserExpect.objects.filter(user=request.session.get("user_id")).values()
        if len(ret) != 0:
            place = ret[0]['tag']
        else:
            place = ''
        return render(request, "expect.html", locals())


def get_recommend(request):
    if models.UserList.objects.count() <= 5:
        recommend_list,rating = problem_recommend.recommend_by_item_id(request.session.get("user_id"))
    else:
        recommend_list, rating = problem_recomm.recommend_by_user_cf(request.session.get("user_id"))
    return render(request, "recommend.html", locals())


def send_page(request):
    return render(request, "send_list.html")


def send_list(request):
    send_list = list(models.ProblemData.objects.filter(sendlist__user=request.session.get("user_id")).values())
    for send in send_list:
        send['send_key'] = 1
    if len(send_list) == 0:
        return JsonResponse({"code": 1, "msg": "没找到需要查询的数据！", "count": "{}".format(len(send_list)), "data": []})
    else:
        return JsonResponse({"code": 0, "msg": "success", "count": "{}".format(len(send_list)), "data": send_list})


def pass_page(request):
    user_obj = models.UserList.objects.filter(user_id=request.session.get("user_id")).first()
    return render(request, "pass_page.html", locals())


def up_info(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        old_pass = request.POST.get("old_pass")
        pass_word = request.POST.get("pass_word")
        user_obj = models.UserList.objects.filter(user_id=request.session.get("user_id")).first()
        if old_pass != user_obj.pass_word:
            return JsonResponse({"Code": 0, "msg": "原密码错误"})
        else:
            models.UserList.objects.filter(user_id=request.session.get("user_id")).update(user_name=user_name,
                                                                                          pass_word=pass_word)
            return JsonResponse({"Code": 0, "msg": "密码修改成功"})


def Heatmap(request):
    codeforces = sql.fetch_codeforces_data(request.session.get("user_id"))
    difficult_level = {}
    tags_level = {}
    for id, data in codeforces.items():
        if data["ac_count"] == 0:
            continue
        difficult = data["rating"]
        tags = data["tags"]
        # 统计每个难度的题目数量
        difficult_level[difficult] = difficult_level.get(difficult, 0) + 1
        # 统计每个标签的题目数量
        for tag in tags:
            tags_level[tag] = tags_level.get(tag, 0) + 1

        # 对标签和难度进行排序
    tag_level = sorted(tags_level.items(), key=operator.itemgetter(1),reverse=True)  # 标签按数量降序排列
    tag_list = [foo[0] for foo in tag_level]  # 获取标签列表
    difficult_level = sorted(difficult_level.items(), key=lambda x: int(x[0]))  # 难度按级别升序排列
    difficult_list = [foo[0] for foo in difficult_level]  # 获取难度列表
    individual_solved = [[0] * len(difficult_list) for _ in range(len(tag_list))]
    # 遍历所有题目，统计不同标签和难度下的通过人数
    for id, data in codeforces.items():
        difficult = data["rating"]
        if difficult in difficult_list:
            difficult_id = difficult_list.index(difficult)  # 获取难度索引
            tags = data["tags"]
            for tag in tags:
                if tag in tag_list:
                    tag_id = tag_list.index(tag)  # 获取标签索引
                    individual_solved[tag_id][difficult_id] += 1  # 记录个人通过数据
    num=[]
    for i in range(len(individual_solved)):
        for j in range(len(individual_solved[i])):
            num.append([i,j,individual_solved[i][j]])
    image_data={
        'tag_list':tag_list,
        'difficult_list':difficult_list,
        'num':num
    }
    return render(request, 'Heatmap.html', image_data)


def radar(request):
    codeforces = sql.fetch_codeforces_data(request.session.get("user_id"))
    # print(codeforces)
    ac_per = {'图论': 0, '数论': 0, '字符串': 0, '动态规划': 0, '数据结构': 0, '其他': 0}
    sub_num = {'图论': 0, '数论': 0, '字符串': 0, '动态规划': 0, '数据结构': 0, '其他': 0}
    ac_num = {'图论': 0, '数论': 0, '字符串': 0, '动态规划': 0, '数据结构': 0, '其他': 0}
    acc = {'图论': 0, '数论': 0, '字符串': 0, '动态规划': 0, '数据结构': 0, '其他': 0}
    # 统计每个标签的题目数量
    tulun = ['dfs and similar', 'graphs', 'trees', 'shortest paths', '2-sat', 'flows', 'graph matchings']
    shulun = ['math', 'combinatorics', 'number theory', 'dsu', 'geometry', 'matrices', 'chinese remainder theorem',
              'fft']
    qita = ['greedy', 'implementation', 'constructive algorithms', 'dp', 'brute force', 'binary search', 'sortings',
            'games', 'probabilities', 'interactive', 'ternary search']
    zifu = ['strings', 'hashing', 'string suffix structures']
    dp = ['dp']
    ds = ['data structures', 'two pointers', 'bitmasks', 'divide and conquer']
    for id, data in codeforces.items():
        tags = data["tags"]
        # print(data)
        for tag in tags:
            if tag in tulun:
                if data["ac_count"] > 0:
                    acc['图论'] += 1
                    ac_num['图论'] += data["ac_count"]
                sub_num['图论'] += data["submission_count"]
            elif(tag in shulun):
                if data["ac_count"] > 0:
                    acc['数论'] += 1
                    ac_num['数论'] += data["ac_count"]
                sub_num['数论'] += data["submission_count"]
            elif(tag in zifu):
                if data["ac_count"] > 0:
                    acc['字符串'] += 1
                    ac_num['字符串'] += data["ac_count"]
                sub_num['字符串'] += data["submission_count"]
            elif(tag in dp):
                if data["ac_count"] > 0:
                    acc['动态规划'] += 1
                    ac_num['动态规划'] += data["ac_count"]
                sub_num['动态规划'] += data["submission_count"]
            elif(tag in ds):
                if data["ac_count"] > 0:
                    acc['数据结构'] += 1
                    ac_num['数据结构'] += data["ac_count"]
                sub_num['数据结构'] += data["submission_count"]
            elif(tag in qita):
                if data["ac_count"] > 0:
                    acc['其他'] += 1
                    ac_num['其他'] += data["ac_count"]
                sub_num['其他'] += data["submission_count"]
    for key, value in ac_per.items():
        ac_per[key] = ac_num[key]/sub_num[key]*100
    image_data={
        'acc':acc,
        'ac_per':ac_per
    }
    return render(request, 'radar.html',image_data)


def chart(request):
    codeforces = sql.fetch_codeforces_data(request.session.get("user_id"))
    difficult_level = {}
    tags_level = {}
    for id, data in codeforces.items():
        if data["ac_count"] == 0:
            continue
        difficult = data["rating"]
        tags = data["tags"]
        # 统计每个难度的题目数量
        difficult_level[difficult] = difficult_level.get(difficult, 0) + 1
        # 统计每个标签的题目数量
        for tag in tags:
            tags_level[tag] = tags_level.get(tag, 0) + 1
    tag_level = sorted(tags_level.items(), key=operator.itemgetter(1), reverse=True)  # 标签按数量降序排列
    tag_list = [foo[0] for foo in tag_level]  # 获取标签列表
    difficult_level = sorted(difficult_level.items(), key=lambda x: int(x[0]))  # 难度按级别升序排列
    difficult_list = [foo[0] for foo in difficult_level]  # 获取难度列表
    image_data = {
        'tag_level': tag_level,
        'tag_list': tag_list,
        'difficult_level': difficult_level,
        'difficult_list': difficult_list
    }
    return render(request, "chart.html",image_data)

