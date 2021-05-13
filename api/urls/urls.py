from rest_framework.urlpatterns import format_suffix_patterns
from api.views import judge
from django.conf.urls import url

from api.crontab.contest import CheckContestStatus

from .contest import urls as curls
from .forum import urls as furls
from .problem import urls as purls
from .user import urls as uurls

urlpatterns = [
    # 验证代码系统
    url(r'^judge/$', judge.JudgeView.as_view()),
    # 定时任务
    url(r'^cron/contests/$', CheckContestStatus.as_view()),
]

urlpatterns += curls + furls + purls + uurls
urlpatterns = format_suffix_patterns(urlpatterns)
