from django.shortcuts import render
from rest_framework.views import APIView
from random import randint
from django_redis import get_redis_connection
from rest_framework.response import Response
import logging
from rest_framework import status
from celery_tasks.sms.tasks import send_sms_code

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):

        # 1. 创建 redis 连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 2. 从 redis 获取发送标记
        send_flag = redis_conn.get('send_flag_%s' % mobile)

        # 3. 如果取到标记，说明此手机号频繁发送短信
        if send_flag:
            return Response({'message': '手机频繁发送短信'}, status=status.HTTP_400_BAD_REQUEST)

        # 4. 生成验证码
        sms_code = '%06d' % randint(0, 999999)
        logger.info(sms_code)

        # 创建 redis 管道：（把多次 redis 操作装入管道中，将来一次性去执行，减少 redis 连接操作）
        pl = redis_conn.pipeline()
        # 5. 把验证码存储到 redis 数据库
        # redis_conn.setex('sms_%s' % mobile, 300, sms_code)  # 300s=5min
        pl.setex('sms_%s' % mobile, 300, sms_code)
        # 6. 存储一个标记，表示此手机号已发送过短信 标记有效期为 60s
        # redis_conn.setex('send_flag_%s' % mobile, 60, 1)
        pl.setex('send_flag_%s' % mobile, 60, 1)

        # 执行管道
        pl.execute()

        # 7. 利用容联云通讯发送短信验证码
        # send_message('1', mobile, (sms_code, 5))
        # 触发异步任务，将异步任务添加到 celery 异步队列
        # send_sms_code(mobile, sms_code)   # 调用普通函数
        send_sms_code.delay(mobile, sms_code)   # 触发异步任务

        # 8. 响应
        return Response({'message': 'ok'})
