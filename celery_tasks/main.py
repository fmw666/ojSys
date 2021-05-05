from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

import os

# 告诉 celery 如果需要使用 Django 配置文件，应该去哪里加载
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# 1. 创建 celery 实例对象
celery_app = Celery('ojsys', broker="redis://127.0.0.1:6379", backend="redis://127.0.0.1:6379")

# 2. 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 3. 自动注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email', 'celery_tasks.judge', 'celery_tasks.timer'])

# 4. 配置定时
celery_app.conf.update(
    CELERYBEAT_SCHEDULE={
        'set_contest_status': {
            'task': 'timer.tasks.set_contest_status',
            'schedule': timedelta(seconds=5),
            # 'args': (5, 6)
        },
    }
)

imports = ('tasks',)
