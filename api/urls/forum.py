from django.conf.urls import url
from api.views import forum


urls = [
    # 获取论坛帖子列表
    url(r'^forums/$', forum.ForumListView.as_view()),
    # 查询论坛帖子例题
    url(r'^forums/(?P<fid>\d+)$', forum.ForumView.as_view()),
    # 发布论坛帖子例题
    url(r'^forums/post/(?P<uid>\d+)$', forum.ForumPostView.as_view()),
]