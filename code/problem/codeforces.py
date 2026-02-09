#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from urllib.request import urlopen, Request
import pymysql.cursors
codeforces = {}
# 发送请求获取 Codeforces 题目集数据
req = Request(
    url="https://codeforces.com/api/problemset.problems",
    headers={'User-Agent': 'Mozilla/5.0'}
)
context = json.loads(urlopen(req).read())  # 解析 JSON 数据
# 遍历题目和题目统计信息
for i, j in zip(context['result']['problems'], context['result']['problemStatistics']):
    contestId = i['contestId']  # 竞赛 ID
    index = i['index']  # 题目索引
    name = i['name']  # 题目名称
    if 'rating' not in i:  # 如果没有评分，跳过该题目
        continue
    rating = i['rating']  # 题目难度
    tags = i['tags']  # 题目标签
    if contestId == 921:  # 跳过 ID 为 921 的竞赛题目
        continue
    problemId = str(contestId) + index
    codeforces[problemId] = {
        'title': name,
        'tags': tags,
        'rating': rating,
        'solved': j['solvedCount'],
    }
    print(codeforces[problemId])

# 连接 MySQL 数据库
connection = pymysql.connect(
        host="localhost",      # 数据库主机
        user="root",           # 用户名
        password="password",   # 密码（替换为你的实际密码）
        database="recommend_problem",  # 数据库名称
        cursorclass=pymysql.cursors.DictCursor
    )
cursor = connection.cursor()
sql="DELETE FROM problem"
cursor.execute(sql)
# 将题目信息插入数据库
for id in codeforces:
    title = codeforces[id]['title']
    title = title.replace(r"'", '')
    tags = ', '.join(codeforces[id]['tags'])
    rating = codeforces[id]['rating']
    solved = codeforces[id]['solved']
    # 生成并执行 SQL 插入语句
    sql = "insert into problem_set values('%s','%s','%s','%s','%s')" % (id, title, tags, rating, solved)
    cursor.execute(sql)
# 提交事务并关闭连接
connection.commit()
cursor.close()
connection.close()
print('插入成功')

