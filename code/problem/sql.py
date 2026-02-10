#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pymysql


# 连接 MySQL 数据库
def fetch_codeforces_data(user):
    """从 MySQL 数据库中读取 Codeforces 题目数据

    使用环境变量优先（与容器运行时的 `MYSQL_*` 保持一致），
    回退到合理默认值以便本地开发。
    """
    host = os.getenv('MYSQL_HOST', '127.0.0.1')
    port = int(os.getenv('MYSQL_PORT', '3306'))
    db_user = os.getenv('MYSQL_USER', 'root')
    db_password = os.getenv('MYSQL_PASSWORD', 'password')
    database = os.getenv('MYSQL_DATABASE', 'recommend_problem')

    connection = pymysql.connect(
        host=host,
        port=port,
        user=db_user,
        password=db_password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4'
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