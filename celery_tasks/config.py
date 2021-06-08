# celery 配置文件
from celery.schedules import crontab
from config import REDIS_SERVER

# 指定任务队列的位置
broker_url = 'redis://' + REDIS_SERVER + '/7'
# 使用redis存储结果
result_backend = 'redis://' + REDIS_SERVER + '/8'

# 指定任务序列化方式
task_serializer = 'json'
# 指定结果序列化方式
result_serializer = 'json'
# 指定任务接受的序列化类型.
accept_content = ['json']
timezone = 'Asia/Shanghai'  # 时区设置
worker_hijack_root_logger = False  # celery默认开启自己的日志，可关闭自定义日志，不关闭自定义日志输出为空
result_expires = 60 * 60 * 24  # 存储结果过期时间（默认1天）

# 导入任务所在文件
# imports = (
#     'celery_tasks.sms.tasks',
#     'celery_tasks.email.tasks',
#     'celery_tasks.judge.tasks',
#     "celery_tasks.timer.tasks",
# )

# 需要执行任务的配置
beat_schedule = {
    "task1": {
        "task": "celery_tasks.timer.tasks.check_contest_status",  # 执行的函数
        "schedule": crontab(minute="*/1"),  # every minute 每分钟执行
        "args": ()  # # 任务函数参数
    },

}
