from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# from ..models.users import User
# from ..serializers.judge import CreateUserSerializer
from celery_tasks.judge.tasks import judge_code
from celery.result import AsyncResult
from celery_tasks.main import celery_app

import os


class JudgeView(APIView):
    # permission_classes = [IsAuthenticated]

    """代码运行"""
    def post(self, request):

        # 验证代码正确性
        res = judge_code.delay(request.data['user_id'], request.data['id'], request.data['code'])
        async_task = AsyncResult(id=res.id, app=celery_app)
        result = async_task.get()

        path = os.path.join(os.getcwd(), 'celery_tasks', 'judge', 'questions', request.data['id'])
        error_path = os.path.join(path, 'error_{}.txt'.format(request.data['user_id']))
        output_path = os.path.join(path, 'out_{}.txt'.format(request.data['user_id']))

        # 文件操作
        error_message = ''
        with open(error_path, 'r') as fp:
            error_message = fp.readlines()

        # 忽略 EOFError 错误
        try:
            if error_message[-1][:8] == 'EOFError':
                error_message = ''
        except:
            pass

        os.remove(error_path)
        os.remove(output_path)

        # 响应
        message = ''
        if error_message:
            result = -1
            message = error_message[-1]
        else:
            message = 'ac' if result == 1 else 'wa'

        return Response({'code': result, 'msg': message})

