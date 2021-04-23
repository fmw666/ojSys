# 编辑异步任务代码
from celery_tasks.sms.ronglian_sms_sdk.sms import send_message
from celery_tasks.main import celery_app


# 使用装饰器注册任务
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    发送短信的 celery 异步任务
    :param mobile: 手机号
    :param sms_code: 验证码
    :return: None
    """
    send_message('1', mobile, (sms_code, 5))
