from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

from ..models.context import Context
from ..serializers.context import ContextSerializer


class ContextListView(ListAPIView):
    """例题列表数据查询"""

    filter_backends = [OrderingFilter]
    ordering_fields = ['id', ]

    serializer_class = ContextSerializer

    def get_queryset(self):
        # alg_type = self.kwargs.get('alg_type')
        # return Problem.objects.filter(alg_type=alg_type)
        return Context.objects.all()


class ContextView(APIView):

    def get(self, request, cid):
        try:
            context = Context.objects.get(id=cid)
        except Context.DoesNotExist:
            raise Http404

        serializer = ContextSerializer(context)
        return Response(serializer.data)
