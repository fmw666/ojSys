from django.conf.urls import url
from api.views import problem

urls = [
    # 获取例题列表
    url(r'^problems/$', problem.ProblemListView.as_view()),
    # 查询单道例题
    url(r'^problems/(?P<pid>\d+)$', problem.ProblemView.as_view()),
]