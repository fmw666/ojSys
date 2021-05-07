from django.conf.urls import url
from api.views import verifications, users

urls = [
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
    # 找回密码
    url(r'^user/forget/$', users.UserPSWForgetView.as_view()),
    # 重设密码
    url(r'^user/password/reset/$', users.UserPSWResetView.as_view()),
    # 更新邮箱
    url(r'^email/$', users.EmailView.as_view()),
    # 激活邮箱
    url(r'^emails/verification/$', users.EmailVerifyView.as_view()),
]