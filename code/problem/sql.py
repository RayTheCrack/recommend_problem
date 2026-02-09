#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
# 连接 MySQL 数据库
def fetch_codeforces_data(user):
    """从 MySQL 数据库中读取 Codeforces 题目数据"""
    connection = pymysql.connect(
        host="localhost",      # 数据库主机
        user="root",           # 用户名
        password="password",   # 密码（替换为你的实际密码）
        database="recommend_problem",  # 数据库名称
        cursorclass=pymysql.cursors.DictCursor
    )
    print(user)
    codeforces = {}  # 存储数据
    try:
        with connection.cursor() as cursor:
            # 查询数据库中的题目信息
            sql = """
                       SELECT ps.id, ps.rating, ps.tags, al.submission_count, al.ac_count
                       FROM problem_set AS ps
                       JOIN accept_list AS al ON ps.id = al.problem_id
                       WHERE al.user_id = %s;
                       """
            cursor.execute(sql,(user,))
            results = cursor.fetchall()
            # 解析数据库返回的数据
            for row in results:
                problem_id = row["id"]
                rating = row["rating"]
                tags = row["tags"]
                if isinstance(tags, str) and tags.strip():  # 确保 tags 不是空字符串
                    tags = [tag.strip() for tag in tags.split(",")]  # 逗号分割并去除空格
                else:
                    tags = []
                submission_count = row["submission_count"]
                ac_count = row["ac_count"]
                codeforces[problem_id] = {
                    "rating": rating,
                    "tags": tags,
                    "submission_count": submission_count,
                    "ac_count": ac_count
                }
    finally:
        connection.close()  # 关闭数据库连接
    return codeforces
# print(codeforces)