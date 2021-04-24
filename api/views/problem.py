from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

from ..models.problem import Problem
from ..serializers.problem import ProblemSerializer


class ProblemListView(ListAPIView):
    """例题列表数据查询"""

    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'header']

    serializer_class = ProblemSerializer

    def get_queryset(self):
        alg_type = self.kwargs.get('alg_type')
        # return Problem.objects.filter(alg_type=alg_type)
        return Problem.objects.all()


class ProblemView(APIView):

    def get(self, request, pid):
        try:
            problem = Problem.objects.get(id=pid)
        except Problem.DoesNotExist:
            raise Http404

        serializer = ProblemSerializer(problem)
        return Response(serializer.data)
