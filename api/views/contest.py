import datetime

from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

from ..models.contest import Contest
from ..models.problem import Problem
from ..models.user.contestorganizer import ContestOrganizer
from ..models.user.user import User
from ..serializers.contest import ContestSerializer


class ContestListView(ListAPIView):
    """例题列表数据查询"""

    filter_backends = [OrderingFilter]
    ordering_fields = ['id', ]

    serializer_class = ContestSerializer

    def get_queryset(self):
        try:
            status = self.request.query_params['status']
        except:
            status = 'sign'
        if status == 'sign':
            return Contest.objects.filter(is_sign=True)
        elif status == 'no':
            return Contest.objects.filter(is_no=True)
        elif status == 'end':
            return Contest.objects.filter(is_end=True)
        elif status == 'start':
            return Contest.objects.filter(is_start=True)
        else:
            return None


class ContestView(APIView):

    @staticmethod
    def get(request, cid):
        try:
            contest = Contest.objects.get(id=cid)
        except Contest.DoesNotExist:
            raise Http404

        serializer = ContestSerializer(contest)
        return Response(serializer.data)


def date_serializer(str_date):
    # str_date: 2021-05-08T08:40:57.000Z   且需要 加 8小时
    fmt = '%Y/%m/%d %H:%M:%S'
    year = str_date.split('-')[0]
    month = str_date.split('-')[1]
    day = str_date.split('-')[2].split('T')[0]
    hour = str_date.split('-')[2].split('T')[1].split(':')[0]
    minute = str_date.split('-')[2].split('T')[1].split(':')[1]
    second = str_date.split('-')[2].split('T')[1].split(':')[2].split('.')[0]
    str_format_date = year + '/' + month + '/' + day + ' ' + hour + ':' + minute + ':' + second

    dt = datetime.datetime.strptime(str_format_date, fmt)
    dt += datetime.timedelta(hours=8)
    return dt


class ContestPostView(APIView):
    @staticmethod
    def post(request, uid):
        # 发布帖子

        name = request.data['name']
        message = request.data['message']
        reward = request.data['reward']
        require = request.data['require']
        problems = request.data['problems']
        # time 需要 加 8小时，且字符串需要转 datetime 2021-05-08T08:40:57.000Z
        sign_up_start_date = date_serializer(request.data['date_sign_up'][0])
        sign_up_end_date = date_serializer(request.data['date_sign_up'][1])
        contest_start_date = date_serializer(request.data['date_contest'][0])
        contest_end_date = date_serializer(request.data['date_contest'][1])

        author = ContestOrganizer.objects.get(user_id=uid)
        contest = Contest.objects.create(name=name, message=message, author=author, reward=reward, requirement=require,
                                         sign_up_start_date=sign_up_start_date, sign_up_end_date=sign_up_end_date,
                                         contest_start_date=contest_start_date, contest_end_date=contest_end_date)
        for pid in problems:
            problem = Problem.objects.get(id=pid)
            contest.problems.add(problem)

        return Response({'code': 1, 'cid': contest.id})
        # return Response({'code': 0})


# 用户报名比赛
class ContestSignView(APIView):
    @staticmethod
    def post(request, cid):
        option = request.data['option']
        uid = request.data['uid']
        user = User.objects.get(id=uid)
        contest = Contest.objects.get(id=cid)

        # 0 只检查是否报名
        if option == 0:
            print(contest.sign_up_user.filter(id=uid))
            try:
                # 如果用户已报名
                if contest.sign_up_user.filter(id=uid):
                    return Response({'code': 1})
                else:
                    return Response({'code': -1})
            except:
                return Response({'code': 0})
        # 1 只进行报名
        elif option == 1:
            try:
                # 如果用户已报名
                if contest.sign_up_user.filter(id=uid):
                    return Response({'code': -1})
                else:
                    contest.sign_up_user.add(user)
                    return Response({'code': 1})
            except:
                return Response({'code': 0})
        # 2 只进行取消报名
        elif option == 2:
            try:
                # 如果用户已报名
                if contest.sign_up_user.filter(id=uid):
                    contest.sign_up_user.remove(user)
                    return Response({'code': 1})
                else:
                    return Response({'code': -1})
            except:
                return Response({'code': 0})
        else:
            Response({'code': 0})

