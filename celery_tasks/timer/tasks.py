from celery_tasks.main import celery_app
from celery import shared_task

from api.models.problem import Problem


@shared_task
@celery_app.task(name='set_contest_status')
def set_contest_status():
    """
    每一分钟进行判断，并设置比赛状态
    :return:
    """
    problem = Problem.objects.get(id=1)
    problem.public = False
    problem.save()

