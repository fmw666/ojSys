from rest_framework import serializers
import re
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings

from ..models.users import User, Participant
from celery_tasks.email.tasks import send_verify_email


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""

    # 序列号器的所有字段：['id', 'username', 'password', 'mobile', 'sms_code', 'allow']
    # 需要校验的字段：['username', 'password', 'mobile', 'sms_code', 'allow']
    # 模型中已存在的字段：['username', 'password', 'mobile']

    # 需要序列号的字段：['id', 'username', 'mobile', 'token']
    # 需要反序列化的字段：['username', 'password', 'mobile', 'sms_code', 'allow']
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'mobile', 'sms_code', 'allow', 'token']
        # 修改字段选项
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                # 'error_message': {
                #     'min_length': '仅允许 5-20 个字符的用户名',
                #     'max_length': '仅允许 5-20 个字符的用户名'
                # }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                # 'error_message': {
                #     'min_length': '仅允许 8-20 个字符的密码',
                #     'max_length': '仅允许 8-20 个字符的密码'
                # }
            }
        }

    @staticmethod
    def validate_mobile(value):
        """单独验证手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    @staticmethod
    def validated_allow(value):
        """是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, attrs):
        """校验验证码"""
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)

        # 向 redis 存储数据时都是以字条串的形式存储的，取出来后都是 bytes 类型
        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validated_data):
        del validated_data['sms_code']
        del validated_data['allow']

        password = validated_data.pop('password')

        user = User(**validated_data)
        # 加密密码
        user.set_password(password)
        user.is_p = True
        user.save()
        # 设置为 普通用户
        participant = Participant(user.id)
        participant.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt中的叫jwt_payload_handler函数(生成payload)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 函数引用 生成jwt

        payload = jwt_payload_handler(user)  # 根据user生成用户相关的载荷
        token = jwt_encode_handler(payload)  # 传入载荷生成完整的jwt

        user.token = token

        return user


class ParticipantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    class Meta:
        model = User
        # fields = ['id', 'username', 'mobile', 'email', 'email_active', 'is_ps', 'participant']
        # fields = '__all__'
        exclude = ['password']

    # is_ps = serializers.BooleanField(source="is_p")
    participant = serializers.SerializerMethodField()

    @staticmethod
    def get_participant(obj):
        participant_data = ParticipantDetailSerializer(obj.participant).data
        return participant_data


class EmailSerializer(serializers.ModelSerializer):
    """更新邮箱序列化器"""
    class Meta:
        model = User
        fields = ['id', 'email']
        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        """重写此方法，发激活邮箱"""
        instance.email = validated_data.get('email')
        instance.save()

        # 发送激活邮箱
        verify_url = instance.generate_email_verify_url()
        send_verify_email.delay(instance.email, verify_url=verify_url)

        return instance
