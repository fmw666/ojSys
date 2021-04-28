from celery_tasks.main import celery_app

from celery_tasks.judge.compiler import run


@celery_app.task(name='celery_tasks.judge.tasks.judge_code')
def judge_code(code, test_code):
    """
    运算代码
    :param code: 代码
    :param test_code: 测试代码片段
    :return:
    """

    # 执行
    return run(code + '\r\n' + test_code)

