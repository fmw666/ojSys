from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
from django.conf import settings

from .problem import Problem


class User(AbstractUser):
    # CompetitionOrganizers
    is_oc = models.BooleanField(default=False, verbose_name='是否 竞赛组织者')
    # Participants
    is_p = models.BooleanField(default=False, verbose_name='是否 参与者')
    # mobile
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号', default='')
    email_active = models.BooleanField(default=False, verbose_name='邮箱激活状态')

    class Meta:
        app_label = 'api'
        # db_table = 'tb_users'
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
        return 'http://127.0.0.1:3000/verify_email?token=' + token

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


# 竞赛发布者
class CompetitionOrganizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()

    class Meta:
        verbose_name = '竞赛发布者（user）'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


# 普通用户
class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')

    solved_problems = models.ManyToManyField(Problem, verbose_name='已解决的题', blank=True)

    # finished_contexts = models.ForeignKey(Context, verbose_name='已参与的竞赛', on_delete=models.DO_NOTHING, related_name='已参与的竞赛')

    class Meta:
        verbose_name = '普通用户（user）'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
