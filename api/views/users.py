from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..models.user.user import User
from ..serializers.users import CreateUserSerializer, UserDetailSerializer, EmailSerializer


class UserView(CreateAPIView):
    """用户注册"""
    # 指定序列号器
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):
    """判断用户名是否被注册"""
    @staticmethod
    def get(request, username):
        # 查询 user 表
        count = User.objects.filter(username=username).count()

        # 包装响应数据
        data = {
            'username': username,
            'count': count
        }

        # 响应
        return Response(data)


class MobileCountView(APIView):
    """判断手机号是否被注册"""
    @staticmethod
    def get(request, mobile):
        # 查询数据库
        count = User.objects.filter(mobile=mobile).count()
        # 构造响应数据
        data = {
            'mobile': mobile,
            'count': count
        }
        # 响应
        return Response(data)


class UserDetailView(RetrieveAPIView):
    """用户详细信息展示"""
    serializer_class = UserDetailSerializer
    # 指定权限，只有通过认证的用户才能访问当前视图
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """重写此方法返回，要展示的用户模型对象"""
        return self.request.user


class UserPSWForgetView(APIView):
    """用户找回密码"""

    def post(self, request):
        mobile = request.data['mobile']
        sms_code = request.data['sms_code']
        code = self.validate(mobile, sms_code)

        return Response({'code': code})

    @staticmethod
    def validate(mobile, sms_code):
        """校验验证码"""
        redis_conn = get_redis_connection('verify_codes')
        real_sms_code = redis_conn.get('sms_%s' % mobile)

        # 向 redis 存储数据时都是以字条串的形式存储的，取出来后都是 bytes 类型
        if real_sms_code is None or sms_code != real_sms_code.decode():
            return 0
        return 1


class UserPSWResetView(APIView):
    """用户重设密码"""
    @staticmethod
    def post(request):
        try:
            user = User.objects.get(mobile=request.data['mobile'])
            user.set_password(request.data['password'])
            user.save()
            code = 1
        except User.DoesNotExist:
            code = 0
        return Response({'code': code})


class EmailView(UpdateAPIView):
    """更新用户邮箱"""
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user


class EmailVerifyView(APIView):
    """激活用户邮箱"""
    @staticmethod
    def get(request):
        # 获取前端查询字符串中传入的 token
        token = request.query_params.get('token')
        # 把 token 解密，并查询对应 user
        user = User.check_verify_email_token(token)
        # 修改当前 user 的 email_active 为 True
        if user is None:
            return Response({'message': '激活失败'}, status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()
        # 响应
        return Response({'message': 'ok'})
