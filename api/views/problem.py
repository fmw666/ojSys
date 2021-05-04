from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

from ..models.problem import Problem
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
                qs = qs.filter(competitionorganizer__user__username=firm) if firm else qs
                qs = qs.filter(header=HEADERS[header]) if header in HEADERS else qs
                return qs
        except:
            return Problem.objects.filter(public=True)


class ProblemView(APIView):

    @staticmethod
    def get(request, pid):
        try:
            problem = Problem.objects.get(id=pid)
        except Problem.DoesNotExist:
            raise Http404

        serializer = ProblemSerializer(problem)
        return Response(serializer.data)
