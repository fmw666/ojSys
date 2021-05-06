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
