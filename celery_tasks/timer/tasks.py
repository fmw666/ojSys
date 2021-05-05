from celery_tasks.main import celery_app
from api.models.problem import Problem


@celery_app.task(name='check_contest_status')
def check_contest_status():
    """
    定时检查比赛状态，并设置
    :return:
    """

    # 执行
    print('我被执行了')
    Problem.objects.filter(id=1).update(public=False)
    return 1

