import datetime

from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.contest import Contest, ContestInfoResult


# d1 > d2  return 1
def compare(d1, d2):
    # d1 > d2  return 1
    if d1.year > d2.year:
        return 1
    elif d1.year < d2.year:
        return -1

    if d1.month > d2.month:
        return 1
    elif d1.month < d2.month:
        return -1

    if d1.day > d2.day:
        return 1
    elif d1.day < d2.day:
        return -1

    if d1.hour > d2.hour:
        return 1
    elif d1.hour < d2.hour:
        return -1

    if d1.minute > d2.minute:
        return 1
    elif d1.minute < d2.minute:
        return -1

    if d1.second > d2.second:
        return 1
    elif d1.second < d2.second:
        return -1

    return 0


class CheckContestStatus(APIView):

    # 按比赛速度排名
    @staticmethod
    def set_contest_result(contest):
        cirs = ContestInfoResult.objects.filter(contest=contest).annotate(Count('pass_problems'))\
            .order_by('-pass_problems__count', 'spend_time')

        # foreach  and  insert
        ranking = 1
        for cir in cirs:
            cir.ranking = ranking
            ranking += 1
            cir.save()

    def get(self, request):
        # 清楚状态（比赛少的时候格式化一下）
        # clear_all_contests_status()
        contests = Contest.objects.all()
        dt_now = datetime.datetime.now()

        for contest in contests:
            # 不检查已经结束的比赛！节约大量时间
            if contest.is_end:
                # 正式项目中不用运行，因为我这里很多测试数据
                # self.set_contest_result(contest)
                continue
            # 报名未开始
            dt_sign_up = contest.sign_up_start_date
            if compare(dt_sign_up, dt_now) == 1:
                contest.is_no = True
                contest.is_sign = False
                contest.is_wait = False
                contest.is_start = False
                contest.is_end = False
            # 比赛开始报名
            dt_sign_end = contest.sign_up_end_date
            if compare(dt_sign_end, dt_now) == 1 and compare(dt_now, dt_sign_up) == 1:
                contest.is_no = False
                contest.is_sign = True
                contest.is_wait = False
                contest.is_start = False
                contest.is_end = False
            # 比赛等待中（报名结束，比赛未开始）
            dt_contest_start = contest.contest_start_date
            if compare(dt_now, dt_sign_end) == 1 and compare(dt_contest_start, dt_now) == 1:
                contest.is_no, contest.is_sign = False, False
                contest.is_wait = True
                contest.is_start, contest.is_end = False, False
            # 比赛开始进行
            dt_contest_end = contest.contest_end_date
            if compare(dt_now, dt_contest_start) == 1 and compare(dt_contest_end, dt_now) == 1:
                contest.is_no = False
                contest.is_sign = False
                contest.is_wait = False
                contest.is_start = True
                contest.is_end = False
            # 比赛结束
            if compare(dt_now, dt_contest_end) == 1:
                contest.is_no = False
                contest.is_sign = False
                contest.is_wait = False
                contest.is_start = False
                contest.is_end = True
                # 计算比赛结果，通过 contest ranking result 表
                self.set_contest_result(contest)
                # 给发布者发短信

            contest.save()

            # 比赛快要（1小时）开始~ 发短信提醒
        return Response({'code': 1})


def clear_all_contests_status():
    contests = Contest.objects.all()
    for contest in contests:
        contest.is_no = False
        contest.is_sign = False
        contest.is_start = False
        contest.is_end = False
        contest.save()
