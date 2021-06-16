# utils
import datetime

# django
from django.http import Http404

# rest_framework
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

# models
from ..models.contest import Contest, ContestInfoResult
from ..models.problem import Problem
from ..models.user.organizer import Organizer
from ..models.user.participant import Participant
from ..models.user.user import User

# serializer
from ..serializers.contest import ContestSerializer
from ..serializers.problem import ProblemSerializer


class ContestsView(ListAPIView):
    ordering_fields = ['id', ]
    serializer_class = ContestSerializer

    def get_queryset(self):
        uid = self.request.query_params['uid']
        return Contest.objects.filter(author_id=uid)


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
            contests = Contest.objects.filter(is_start=True)
            if user.is_p:
                p_contests = Participant.objects.get(user=user).sign_up_contests.all()
                return contests & p_contests
            elif user.is_oc:
                co = Organizer.objects.get(user=user)
                return contests.filter(author=co)
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

        author = Organizer.objects.get(user_id=uid)
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
    @staticmethod
    def post(request, cid):
        # 排名情况后台 crontab 里自己计算，设置这个人已完成比赛，报名比赛取消该比赛
        uid = request.data['uid']
        problems = request.data['problems']
        spend_time = request.data['spend_time']
        # 换成 reduce 可，但这里就三条，固定的
        spend_time_str = '{0}h{1}m{2}s'.format(spend_time[0], spend_time[1], spend_time[2])
        contest = Contest.objects.get(id=cid)
        user = User.objects.get(id=uid)
        contest.commit_user.add(user)
        cir = ContestInfoResult.objects.create(user_id=uid, contest=contest, spend_time=spend_time_str)
        for pid in problems:
            problem = Problem.objects.get(id=pid)
            cir.pass_problems.add(problem)
        cir.save()
        p_user = Participant.objects.get(user=user)
        p_user.sign_up_contests.remove(contest)
        p_user.finished_contests.add(contest)
        return Response({'code': 1})


# 获取比赛排名情况
class ContestRankingView(APIView):
    @staticmethod
    def get(request, cid):
        try:
            contest = Contest.objects.get(id=cid)
        except Contest.DoesNotExist:
            return Response({'code': 0})
        # 报名提交用户
        commit_users = contest.commit_user.all()
        commit_users_json = []
        for cu in commit_users:
            commit_users_json.append([cu.username, cu.id])

        # 排名情况
        cirs = ContestInfoResult.objects.all().order_by('ranking')
        # 排名记录
        rankings_json = []
        for cir in cirs:
            rj = {'user': [], 'pass_problems': [], 'spend_time': []}
            rj['user'].append([cir.user.id, cir.user.username])
            rj['pass_problems'].append([[pp.id, pp.name] for pp in cir.pass_problems.all()])
            rj['spend_time'].append(cir.spend_time)
            rankings_json.append(rj)

        # 比赛所有题目
        problems_json = []
        for p in contest.problems.all():
            problems_json.append([p.name, p.id])

        return Response({'code': 1, 'commit_users': commit_users_json,
                         'rankings': rankings_json, 'problems': problems_json})
