# django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# utils
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
from config import FRONT_URL


class User(AbstractUser):
    # User identity: o -> Organizer, p -> Participant
    is_o = models.BooleanField(default=False, verbose_name='是否 竞赛组织者')
    is_p = models.BooleanField(default=False, verbose_name='是否 竞赛参与者')
    is_admin = models.BooleanField(default=False, verbose_name='是否 管理员')

    # Verification information: mobile & email
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号', default='')
    email = models.EmailField()
    email_active = models.BooleanField(default=False, verbose_name='邮箱激活状态')

    # Validate user identity
    def clean(self, *args, **kwargs):
        # run the base validation
        super(User, self).clean()

        # Only allow one of the identity
        if [self.is_o, self.is_p, self.is_admin].count(True) > 1:
            self.is_o, self.is_p, self.is_admin = False, False, False

    class Meta:
        app_label = 'api'
        verbose_name = '用户大类（user）'
        verbose_name_plural = verbose_name

    def generate_email_verify_url(self):
        """生成邮箱激活链接"""
        # 1. 创建加密序列化器
        serializer = TJWSSerializer(settings.SECRET_KEY, 3600 * 24)

        # 2. 调用 dumps 方法进行加密，bytes
        data = {'user_id': self.id, 'email': self.email}
        token = serializer.dumps(data).decode()

        # 3. 拼接激活 url
        return FRONT_URL + '/verify_email?token=' + token

    @staticmethod
    def check_verify_email_token(token):
        """对 token 解密并查询对应的 user"""
        # 1. 创建加密序列化器
        serializer = TJWSSerializer(settings.SECRET_KEY, 3600 * 24)
        # 2. 用 loads 解密
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            uid = data.get('user_id')
            email = data.get('email')
            try:
                user = User.objects.get(id=uid, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user
