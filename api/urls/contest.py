from django.conf.urls import url
from api.views import contest

urls = [
    # 获取比赛列表
    url(r'^contests/$', contest.ContestListView.as_view()),
    # 查询单个比赛
    url(r'^contests/(?P<cid>\d+)$', contest.ContestView.as_view()),
    # 查询单个比赛的所有题目
    url(r'^contests/(?P<cid>\d+)/problems/$', contest.ContestAllProblemsView.as_view()),
    # 发布比赛
    url(r'^contests/post/(?P<uid>\d+)$', contest.ContestPostView.as_view()),

    # 用户报名比赛
    url(r'^contest/(?P<cid>\d+)/sign/$', contest.ContestSignView.as_view()),
    # 提交用户记录
    url(r'^contest/(?P<cid>\d+)/info/$', contest.ContestInfoView.as_view()),
]
