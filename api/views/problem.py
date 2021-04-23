from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.problem import Problem


class ProblemsView(APIView):
    """例题列表"""
    def get(self, request):
        problems = Problem.objects.all()
        return Response({'code': 1, 'msg': '', 'problems': problems.count()})
