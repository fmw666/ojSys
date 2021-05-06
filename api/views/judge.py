from rest_framework.views import APIView
from rest_framework.response import Response

from celery_tasks.judge.tasks import judge_code
from celery.result import AsyncResult
from celery_tasks.main import celery_app

from ..models.problem import Problem


class JudgeView(APIView):
    # permission_classes = [IsAuthenticated]

    """代码运行"""
    @staticmethod
    def post(request):

        pid = request.data['id']
        code = request.data['code']

        problem = Problem.objects.get(id=pid)
        test_code = problem.test_code

        # 验证代码正确性
        res = judge_code.delay(code, test_code)
        async_task = AsyncResult(id=res.id, app=celery_app)
        result = async_task.get()

        if result['output'] != '':
            result['output'] = result['output'].split('.py')[1][3:]
            if result['output'].count('不等于正确值'):
                result['output'] = '答案错误' + result['output'].split('Exception')[-1]

        return Response(result)
