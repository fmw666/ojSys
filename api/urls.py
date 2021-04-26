from django.urls import re_path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import drf, verifications, users, judge, problem, context

urlpatterns = [
    re_path(r'^articles/$', drf.ArticleList.as_view()),
    re_path(r'^articles/(?P<pk>[0-9]+)$', drf.ArticleDetail.as_view()),
    # 发短信
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', verifications.SMSCodeView.as_view()),
    # 注册用户
    url(r'^users/$', users.UserView.as_view()),
    # 判断用户名是否已经注册
    url(r'^users/username/(?P<username>\w{5,20})/count/$', users.UsernameCountView.as_view()),
    # 判断手机号是否已经注册
    url(r'^users/mobile/(?P<mobile>1[3-9]\d{9})/count/$', users.MobileCountView.as_view()),
    # 获取用户详情
    url(r'^user/$', users.UserDetailView.as_view()),
    # 更新邮箱
    url(r'^email/$', users.EmailView.as_view()),
    # 激活邮箱
    url(r'^emails/verification/$', users.EmailVerifyView.as_view()),

    # 验证代码系统
    url(r'^judge/$', judge.JudgeView.as_view()),

    # 获取例题列表
    url(r'^problems/$', problem.ProblemListView.as_view()),
    # 查询例题
    # url(r'^problems/(?P<p_id>\d+)', problem.ProblemListView.as_view()),
    # 查询单道例题
    url(r'^problems/(?P<pid>\d+)$', problem.ProblemView.as_view()),

    # 获取比赛列表
    url(r'^contexts/$', context.ContextListView.as_view()),
    # 查询例题
    # url(r'^contexts/(?P<c_id>\d+)', context.ContextListView.as_view()),
    # 查询单道例题
    url(r'^contexts/(?P<cid>\d+)$', context.ContextView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
