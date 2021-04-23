from celery_tasks.main import celery_app
from django.core.mail import send_mail
from django.conf import settings


@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """
    发激活邮箱的邮件
    :param to_email: 收件人邮箱
    :param verify_url: 邮箱激活 url
    :return:
    """

    title = '重置您的 <敲哈儿码都> 密码'
    msg = '找回密码'
    from_email = settings.DEFAULT_FROM_EMAIL
    receivers = [to_email, ]

    # 渲染模板
    html_str = '<p>尊敬的用户您好！</p>'\
               '<p>感谢您使用</p>'\
               '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>'\
               '<p><a href="%s">%s</a></p>' % (to_email, verify_url, verify_url)

    send_mail(
        title,
        msg,
        from_email,
        receivers,
        # 发送异常时不提示
        # fail_silently=True,
        html_message=html_str
    )
