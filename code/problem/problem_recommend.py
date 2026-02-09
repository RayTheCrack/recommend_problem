#!/usr/bin/python3.9.10
# -*- coding: utf-8 -*-
# @Time    : 2023/2/18 9:41
# @File    : problem_recommend.py
import os
import sys

sys.path.append(r"C:\Users\18454\Desktop\recommend_problem (3)\recommend_problem\code")
os.environ["DJANGO_SETTINGS_MODULE"] = "problemRecommend.settings"
import django
import requests
django.setup()
from problem import models
from math import sqrt, pow
import operator
from django.db.models import Subquery, Q, Count
import random


# 计算两个题目之间的相似度，采用的是余弦相似度计算方法
def similarity(problem1_id, problem2_id):
    problem1_set = models.SendList.objects.filter(problem=problem1_id)
    # problem1的投递用户数
    problem1_sum = problem1_set.count()
    problem2_sum = models.SendList.objects.filter(problem=problem2_id).count()
    # 两者的交集
    common = models.SendList.objects.filter(user__in=Subquery(problem1_set.values('user')), problem=problem2_id).values('user').count()
    if problem1_sum == 0 or problem2_sum == 0:
        return 0
    similar_value = common / sqrt(problem1_sum * problem2_sum)  # 余弦计算相似度
    return similar_value


# 基于物品的协同过滤推荐算法
def recommend_by_item_id(user_id, k=20):
    # 投递简历最多的前三keyword
    problems_id = models.SendList.objects.filter(user_id=user_id).values('problem_id')  # 先找出用户提交过的题目
    key_word_list = []
    for problem in problems_id:
        key_word_list.extend(list(models.ProblemData.objects.get(ID=problem['problem_id']).Tags.split(', ')))
    key_word_list_1 = list(set(key_word_list))
    user_prefer = []
    for key_word in key_word_list_1:
        user_prefer.append([key_word, key_word_list.count(key_word)])
    user_prefer = sorted(user_prefer, key=lambda x:x[1])  # 排序
    user_prefer = [x[0] for x in user_prefer[0:9]]  # 找出最多的9个的key_word
    current_user = models.UserList.objects.get(user_id=user_id)
    rating = models.UserList.objects.get(user_id=user_id).rating
    un_send = list(models.ProblemData.objects.filter(
        ~Q(sendlist__user=user_id),  # 排除该用户已提交题目
    ).values())

    filtered_problems = []
    for problem in un_send:
        tags = problem['Tags'].split(', ')  # 将 Tags 字段按 ', ' 拆分成标签列表
        if any(tag in user_prefer for tag in tags):  # 如果 Tags 中任意一个标签在 user_prefer 列表中
            filtered_problems.append(problem)

    un_send = random.sample(filtered_problems, 30)  # 随机挑选 30 个题目
    # 如果当前用户没有提交过题目,则推荐用户相对薄弱算法方面且符合用户水平的题目
    if current_user.sendlist_set.count() == 0:
        problem_list=[]
        for un_send_problem in un_send:
            Rating = int(un_send_problem['Rating'])
            if abs(rating - Rating) <= 500:
                problem_list.append(un_send_problem)
        problem_list = random.sample(problem_list, 9)
        return problem_list,1500
    send = []
    for problem in problems_id:
        send.append(models.ProblemData.objects.filter(ID=problem['problem_id']).values()[0])
    distances = []
    names = []
    # 在未提交过的题目中找到
    for un_send_problem in un_send:
        for send_problem in send:
            if un_send_problem not in names:
                names.append(un_send_problem)
                Rating=int(un_send_problem['Rating'])
                if abs(rating-Rating) <=500:
                    distances.append((similarity(un_send_problem['ID'], send_problem['ID']), un_send_problem))
    distances.sort(key=lambda x: x[0], reverse=True)
    recommend_list = []
    for mark, problem in distances:
        if len(recommend_list) >= k:
            break
        if problem not in recommend_list:
            recommend_list.append(problem)
    recommend_list = random.sample(recommend_list, 9)
    return recommend_list,int(rating)


if __name__ == '__main__':
    recommend_by_item_id(1)
