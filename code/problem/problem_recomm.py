import os
import sys
import django
import requests
from django.db.models import Subquery, Q, Count, Sum
import random
from math import sqrt

# 设置Django环境
sys.path.append(r"C:\Users\18454\Desktop\recommend_problem (3)\recommend_problem\code")
os.environ["DJANGO_SETTINGS_MODULE"] = "problemRecommend.settings"
django.setup()

from problem import models


def user_similarity(user1_id, user2_id):
    """计算两个用户之间的相似度，基于共同投递的题目数量"""
    user1_problems = models.SendList.objects.filter(user=user1_id).values('problem')
    user1_count = user1_problems.count()
    if user1_count == 0:
        return 0

    user2_problems = models.SendList.objects.filter(user=user2_id)
    user2_count = user2_problems.count()
    if user2_count == 0:
        return 0
    common = user2_problems.filter(problem__in=Subquery(user1_problems)).count()
    return common / sqrt(user1_count * user2_count)

def recommend_by_user_cf(user_id, k=20):
    try:
        user = models.UserList.objects.get(user_id=user_id)
    except models.UserList.DoesNotExist:
        return [], 1500
    # 获取用户信息和能力评级
    user_rating = models.UserList.objects.get(user_id=user_id).rating
    sent_problems = models.SendList.objects.filter(user=user).values_list('problem_id', flat=True)
    preferred_tags = models.UserExpect.objects.filter(user=user_id).values_list('tag', flat=True)
    # 计算与其他用户的相似度
    all_users = models.UserList.objects.exclude(user_id=user_id)
    sim_users = []
    for user in all_users:
        sim_users.append((user, abs(user_rating-models.UserList.objects.get(user_id=user.user_id).rating)))
    sim_users.sort(key=lambda x: x[1])
    all_users = [uid for uid, _ in sim_users[:15]]
    similarities = []
    for other_user in all_users:
        sim = user_similarity(user_id, other_user.user_id)
        if sim > 0:
            similarities.append((other_user.user_id, sim))
    # 按相似度降序排序，取前10个相似用户
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_users = [uid for uid, _ in similarities[:10]]
    # 没有相似用户时退回热门题目推荐
    if not top_users:
        return fallback_recommendation(sent_problems, user_rating, 9)
    # 收集相似用户的题目并计算推荐得分
    problem_scores = {}
    user_sim_map = dict(similarities[:10])
    # 获取相似用户的所有有效题目
    candidate_entries = models.SendList.objects.filter(
        user_id__in=top_users
    ).exclude(problem_id__in=sent_problems).select_related('problem')
    # 计算题目得分（相似度加权）
    for entry in candidate_entries:
        pid = entry.problem_id
        score = user_sim_map.get(entry.user_id, 0)
        problem_scores[pid] = problem_scores.get(pid, 0) + score
    # 按得分排序并筛选符合难度要求的题目
    sorted_problems = sorted(problem_scores.items(), key=lambda x: x[1], reverse=True)
    recommendations = []
    preferred = list(preferred_tags.values_list('tag', flat=True))
    for pid, _ in sorted_problems:
        try:
            problem = models.ProblemData.objects.get(ID=pid)
            tags = problem['Tags'].split(', ')
            if any(tag in tags for tag in preferred) and abs(int(problem.Rating) - user_rating) <= 500:
                recommendations.append(problem)
                if len(recommendations) >= 9:
                    break
        except models.ProblemData.DoesNotExist:
            continue
    for pid, _ in sorted_problems:
        try:
            problem = models.ProblemData.objects.get(ID=pid)
            if abs(int(problem.Rating) - user_rating) <= 500 and problem not in recommendations:
                recommendations.append(problem)
                if len(recommendations) >= k:
                    break
        except models.ProblemData.DoesNotExist:
            continue
    # 补足推荐数量
    if len(recommendations) < k:
        needed = k - len(recommendations)
        additional = get_fallback_problems(sent_problems, user_rating, needed)
        recommendations.extend(additional)
    recommendations = random.sample(recommendations, 9)
    return recommendations, int(user_rating)

def fallback_recommendation(sent_problems, user_rating, k):
    """退回策略：选择符合难度要求且未提交的题目"""
    candidates = models.ProblemData.objects.exclude(ID__in=sent_problems).filter(
        Rating__gte=user_rating - 500,
        Rating__lte=user_rating + 500
    ).order_by('?')[:k * 2]
    return random.sample(list(candidates), min(k, len(candidates)))


def get_fallback_problems(sent_problems, user_rating, num):
    """获取补充题目"""
    return list(models.ProblemData.objects.exclude(ID__in=sent_problems).filter(
        Rating__gte=user_rating - 500,
        Rating__lte=user_rating + 500
    ).order_by('?')[:num])


if __name__ == '__main__':
    # 示例：为用户ID为1的用户推荐题目
    recommendations, rating = recommend_by_user_cf(1)