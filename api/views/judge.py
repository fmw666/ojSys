from rest_framework.views import APIView
from rest_framework.response import Response

from ..models.users import User
# from ..serializers.judge import CreateUserSerializer
from celery_tasks.judge.tasks import judge_code
from celery.result import AsyncResult
from celery_tasks.main import celery_app

from ..models.problem import Problem


class JudgeView(APIView):
    # permission_classes = [IsAuthenticated]

    """代码运行"""
    def post(self, request):

        pid = request.data['id']
        user_id = request.data['user_id']
        code = request.data['code']

        problem = Problem.objects.get(id=pid)
        data_in = problem.inputs
        data_cor_output = problem.correct_outs

        # 验证代码正确性
        res = judge_code.delay(code, data_in, data_cor_output)
        async_task = AsyncResult(id=res.id, app=celery_app)
        result = async_task.get()

        return Response(result)
