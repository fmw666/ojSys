from django.conf.urls import url
from api.views import contest

urls = [
    # 获取比赛列表
    url(r'^contests/$', contest.ContestListView.as_view()),
    # 查询单道例题
    url(r'^contests/(?P<cid>\d+)$', contest.ContestView.as_view()),
]