# django
from django.http import Http404

# rest_framework
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

# models
from ..models.forum import Forum
from ..models.user.user import User

# serializer
from ..serializers.forum import ForumSerializer


class ForumListView(ListAPIView):
    """例题列表数据查询"""

    filter_backends = [OrderingFilter]
    ordering_fields = ['publish_date', ]

    serializer_class = ForumSerializer

    def get_queryset(self):
        try:
            from_who = self.request.query_params['from']
        except ModuleNotFoundError:
            from_who = 'all'

        if from_who == 'all':
            return Forum.objects.all()
        # 热门为，点赞数最多的前10个
        elif from_who == 'hot':
            # return Forum.objects.all()
            return Forum.objects.all().order_by('-like_cnt', '-publish_date')
        elif from_who == 'user':
            return Forum.objects.filter(author__is_p=True)
        elif from_who == 'og':
            return Forum.objects.filter(author__is_oc=True)
        elif from_who == 'admin':
            return Forum.objects.filter(author__is_admin=True)
        else:
            return None


class ForumView(APIView):

    @staticmethod
    def get(request, fid):
        try:
            forum = Forum.objects.get(id=fid)
        except Forum.DoesNotExist:
            raise Http404

        serializer = ForumSerializer(forum)
        return Response(serializer.data)

    @staticmethod
    def post(request, fid):
        # 点赞操作
        if request.data['option'] == 0:
            try:
                uid = request.data['uid']
                user = User.objects.get(id=uid)
                forum = Forum.objects.get(id=fid)
                forum.like_cnt.add(user)
                forum.save()
                return Response({'code': 1})
            except User.DoesNotExist or Forum.DoesNotExist:
                return Response({'code': 0})

        # 取消点赞
        elif request.data['option'] == 1:
            try:
                uid = request.data['uid']
                user = User.objects.get(id=uid)
                forum = Forum.objects.get(id=fid)
                forum.like_cnt.remove(user)
                forum.save()
                return Response({'code': 1})
            except User.DoesNotExist or Forum.DoesNotExist:
                return Response({'code': 0})


class ForumPostView(APIView):
    @staticmethod
    def post(request, uid):
        # 发布帖子
        try:
            title = request.data['title']
            content = request.data['content']
            user = User.objects.get(id=uid)

            forum = Forum.objects.create(title=title, content=content, author=user)
            return Response({'code': 1, 'fid': forum.id})
        except User.DoesNotExist or Forum.DoesNotExist:
            return Response({'code': 0})
