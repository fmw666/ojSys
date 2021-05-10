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
from ..serializers.problem import ProblemSerializer


class ContestListView(ListAPIView):
    """例题列表数据查询"""

    filter_backends = [OrderingFilter]
    ordering_fields = ['id', ]

    serializer_class = ContestSerializer

    def get_queryset(self):
        status = self.request.query_params['status'] if 'status' in self.request.query_params else 'sign'
        if status == 'sign':
            return Contest.objects.filter(is_sign=True)
        elif status == 'no':
            return Contest.objects.filter(is_no=True)
        elif status == 'end':
            return Contest.objects.filter(is_end=True)
        elif status == 'start':
            # 返回给普通用户他们报名的比赛，或者竞赛发布者他们发布的正在进行的比赛
            uid = self.request.query_params['uid']
            user = User.objects.get(id=uid)
            contest = Contest.objects.filter(is_start=True)
            if user.is_p:
                return contest.filter(sign_up_user=uid)
            elif user.is_oc:
                co = ContestOrganizer.objects.get(user=user)
                return contest.filter(author=co)
        else:
            return None


# 获取比赛所有题目
class ContestAllProblemsView(ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        cid = self.kwargs.get('cid')
        uid = self.request.query_params['uid']
        try:
            contest = Contest.objects.get(id=cid)
        except Contest.DoesNotExist:
            return None

        user = User.objects.get(id=uid)
        # 如果没有该用户，就返回 空 QuerySet，或者是管理员或者竞赛发布者可以看
        if contest.sign_up_user.filter(id=uid) or user.is_oc or user.is_admin:
            return contest.problems.all()
        else:
            return contest.sign_up_user.filter(id=uid)


class ContestView(APIView):

    @staticmethod
    def get(request, cid):
        try:
            contest = Contest.objects.get(id=cid)
        except Contest.DoesNotExist:
            raise Http404

        serializer = ContestSerializer(contest)
        return Response(serializer.data)


# 日期序列化
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


# 管理人发布竞赛
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
            try:
                # 如果用户已报名
                if contest.sign_up_user.filter(id=uid):
                    return Response({'code': 1})
                else:
                    return Response({'code': -1})
            except Contest.DoesNotExist:
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
            except Contest.DoesNotExist:
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
            except Contest.DoesNotExist:
                return Response({'code': 0})
        else:
            Response({'code': 0})


# 用户提交比赛添加
class ContestInfoView(APIView):
    pass
