from django.contrib.auth.backends import ModelBackend
import re

from api.models.drf import User


def jwt_response_payload_handler(token, user=None, request=None):
    """重新 JWT 登录视图的构造响应数据函数，多追加 id 及 username"""

    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_account(account):
    """
    通过传入的账号动态获取 user 模型对象
    :param account: 有可能是手机号，有可能是用户名
    :return: user 或 None
    """
    try:
        if re.match(r'1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """修改 Django 的认证类，为了实现多账号登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 获取到 user
        user = get_user_by_account(username)
        # 判断当前前端传入的密码是否正确
        if user and user.check_password(password):
            # 返回 user
            return user
