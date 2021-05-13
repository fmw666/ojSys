from django.conf.urls import url
from api.views import problem

urls = [
    # 获取例题列表
    url(r'^problems/$', problem.ProblemListView.as_view()),
    # 查询单道例题
    url(r'^problems/(?P<iid>\d+)$', problem.ProblemView.as_view()),

    # 得到排名情况
    url(r'^problems/ranking/$', problem.RankingView.as_view()),
    # 查询发布者自己发布的题目
    url(r'^problems/my/$', problem.ProblemListOfMineView.as_view()),
    # 查询发布者自己发布的题目
    url(r'^problems/id/$', problem.ProblemIdView.as_view()),
]
