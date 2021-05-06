from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import verifications, users, judge, problem, contest, forum

urlpatterns = [
    # 发短信
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', verifications.SMSCodeView.as_view()),
    # 注册用户
    url(r'^users/$', users.UserView.as_view()),
    # 判断用户名是否已经注册
    url(r'^users/username/(?P<username>\w{3,20})/count/$', users.UsernameCountView.as_view()),
    # 判断手机号是否已经注册
    url(r'^users/mobile/(?P<mobile>1[3-9]\d{9})/count/$', users.MobileCountView.as_view()),
    # 获取用户详情
    url(r'^user/$', users.UserDetailView.as_view()),
    # 判断帖子发的数量
    url(r'^user/forums/(?P<uid>\d+)/count/$', users.ForumCountView.as_view()),
    # 找回密码
    url(r'^user/forget/$', users.UserPSWForgetView.as_view()),
    # 重设密码
    url(r'^user/password/reset/$', users.UserPSWResetView.as_view()),
    # 更新邮箱
    url(r'^email/$', users.EmailView.as_view()),
    # 激活邮箱
    url(r'^emails/verification/$', users.EmailVerifyView.as_view()),

    # 验证代码系统
    url(r'^judge/$', judge.JudgeView.as_view()),

    # 获取例题列表
    url(r'^problems/$', problem.ProblemListView.as_view()),
    # 查询单道例题
    url(r'^problems/(?P<pid>\d+)$', problem.ProblemView.as_view()),

    # 获取比赛列表
    url(r'^contests/$', contest.ContestListView.as_view()),
    # 查询单道例题
    url(r'^contests/(?P<cid>\d+)$', contest.ContestView.as_view()),

    # 获取论坛帖子列表
    url(r'^forums/$', forum.ForumListView.as_view()),
    # 查询论坛帖子例题
    url(r'^forums/(?P<fid>\d+)$', forum.ForumView.as_view()),
    # 发布论坛帖子例题
    url(r'^forums/post/(?P<uid>\d+)$', forum.ForumPostView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
