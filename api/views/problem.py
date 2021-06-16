# django
from django.db.models import Count
from django.http import Http404

# rest_framework
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

# models
from ..models.problem import Problem
from ..models.user.participant import Participant
from ..models.user.organizer import Organizer
from ..models.user.user import User

# serializer
from ..serializers.problem import ProblemSerializer

ALGS = {
    '基础': 'b',
    '贪心算法': 'g',
    'DFS/BFS': 'f',
    '动态规划': 'x',
    '二分法': 't',
    '最短路径算法': 'd'
}
DSS = {
    '基础': 'b',
    '数组': 'a',
    '链表': 'l',
    '栈': 's',
    '队列': 'q',
    '哈希表': 'h',
    '树': 't',
    '图': 'p'
}
HEADERS = {
    '入门': 'a',
    '简单': 'b',
    '中等': 'c',
    '困难': 'd',
    '特难': 'e',
}


class ProblemListView(ListAPIView):
    """例题列表数据查询"""

    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'header']

    serializer_class = ProblemSerializer

    def get_queryset(self):
        try:
            alg = self.request.query_params['alg']
            ds = self.request.query_params['ds']
            firm = self.request.query_params['firm']
            header = self.request.query_params['header']
            # 如果都没有
            if not alg and not ds and not firm and not header:
                # 查询全部
                return Problem.objects.filter(public=True)
            else:
                qs = Problem.objects.filter(public=True)
                qs = qs.filter(alg_type=ALGS[alg]) if alg in ALGS else qs
                qs = qs.filter(ds_type=DSS[ds]) if ds in DSS else qs
                qs = qs.filter(contestorganizer__user__username=firm) if firm else qs
                qs = qs.filter(header=HEADERS[header]) if header in HEADERS else qs
                return qs
        except:
            return Problem.objects.filter(public=True)


# 发布者自己发布的题目列表
class ProblemListOfMineView(ListAPIView):
    ordering_fields = ['id']
    serializer_class = ProblemSerializer

    def get_queryset(self):
        try:
            uid = self.request.query_params['uid']
            user = User.objects.get(id=uid)
            problem = Problem.objects.filter(author=user)
        except Problem.DoesNotExist:
            raise Http404

        return problem


class ProblemView(APIView):
    @staticmethod
    def get(request, iid):
        try:
            problem = Problem.objects.get(id=iid)
        except Problem.DoesNotExist:
            raise Http404

        serializer = ProblemSerializer(problem)
        return Response(serializer.data)

    @staticmethod
    def post(request, iid):
        try:
            user = User.objects.get(id=iid)
        except Organizer.DoesNotExist:
            raise Http404
        name = request.data['name']
        message = request.data['message']
        challenge = request.data['challenge']
        input_example = request.data['input_example']
        output_example = request.data['output_example']
        alg_type = ALGS[request.data['alg_type']] if request.data['alg_type'] in ALGS else 'b'
        ds_type = DSS[request.data['ds_type']] if request.data['ds_type'] in DSS else 'b'
        header = HEADERS[request.data['header']] if request.data['header'] in HEADERS else 'a'

        init_code = request.data['init_code']
        test_code = request.data['test_code']
        public = False if request.data['open'] == 'no' else True

        try:
            problem = Problem.objects.create(name=name, message=message, challenge=challenge, author=user,
                                             input_example=input_example, output_example=output_example,
                                             alg_type=alg_type, ds_type=ds_type, header=header,
                                             init_code=init_code, test_code=test_code, public=public)
            return Response({'code': 1})
        except Problem.DoesNotExist:
            return Response({'code': 0})


# 排名情况
class RankingView(APIView):

    @staticmethod
    def get(request):
        return Response(Participant.objects.values('user__username')
                        .annotate(Count('solved_problems'))
                        .order_by('-solved_problems__count'))


# 得到题目 id
class ProblemIdView(APIView):
    @staticmethod
    def get(request):
        option = request.query_params['option']

        cur_id = request.query_params['cur_id']
        problems = Problem.objects.filter(public=True).order_by('id')
        for index, problem in enumerate(problems):
            if str(problem.id) == cur_id:
                # 下一题
                if option == '1':
                    if index + 1 < len(problems):
                        return Response({'code': 1, 'pid': problems[index + 1].id})
                    else:
                        return Response({'code': 1, 'pid': problems[0].id})
                # 上一题
                elif option == '-1':
                    if index - 1 >= 0:
                        return Response({'code': 1, 'pid': problems[index - 1].id})
                    else:
                        return Response({'code': 1, 'pid': problems[len(problems) - 1].id})
        return Response({'code': 0})
