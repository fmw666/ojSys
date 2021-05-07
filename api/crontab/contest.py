import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.contest import Contest


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

    @staticmethod
    def get(request):
        # 清楚状态（比赛少的时候格式化一下）
        # clear_all_contests_status()
        contests = Contest.objects.all()
        dt_now = datetime.datetime.now()

        for contest in contests:
            # 不检查已经结束的比赛！节约大量时间
            if contest.is_end:
                continue
            # 报名未开始
            dt_sign_up = contest.sign_up_start_date
            if compare(dt_sign_up, dt_now) == 1:
                contest.is_no = True
                contest.is_sign = False
                contest.is_start = False
                contest.is_end = False
            # 比赛开始报名
            dt_sign_end = contest.sign_up_end_date
            if compare(dt_sign_end, dt_now) == 1 and compare(dt_now, dt_sign_up) == 1:
                contest.is_no = False
                contest.is_sign = True
                contest.is_start = False
                contest.is_end = False
            # 比赛开始进行
            dt_contest_start = contest.contest_start_date
            dt_contest_end = contest.contest_end_date
            if compare(dt_now, dt_contest_start) == 1 and compare(dt_contest_end, dt_now) == 1:
                contest.is_no = False
                contest.is_sign = False
                contest.is_start = True
                contest.is_end = False
            # 比赛结束
            if compare(dt_now, dt_contest_end) == 1:
                contest.is_no = False
                contest.is_sign = False
                contest.is_start = False
                contest.is_end = True

            contest.save()
        return Response({'code': 1})


def clear_all_contests_status():
    contests = Contest.objects.all()
    for contest in contests:
        contest.is_no = False
        contest.is_sign = False
        contest.is_start = False
        contest.is_end = False
        contest.save()
