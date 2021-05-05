from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

from ..models.contest import Contest
from ..serializers.contest import ContestSerializer


class ContestListView(ListAPIView):
    """例题列表数据查询"""

    filter_backends = [OrderingFilter]
    ordering_fields = ['id', ]

    serializer_class = ContestSerializer

    def get_queryset(self):
        # alg_type = self.kwargs.get('alg_type')
        # return Problem.objects.filter(alg_type=alg_type)
        return Contest.objects.all()


class ContestView(APIView):

    @staticmethod
    def get(request, cid):
        try:
            contest = Contest.objects.get(id=cid)
        except Contest.DoesNotExist:
            raise Http404

        serializer = ContestSerializer(contest)
        return Response(serializer.data)
