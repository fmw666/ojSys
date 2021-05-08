from django.db import models

from .user import User
from ..problem import Problem
from ..contest import Contest


# 普通用户
class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')

    solved_problems = models.ManyToManyField(Problem, verbose_name='已解决的题', blank=True)
    sign_up_contests = models.ManyToManyField(Contest, verbose_name='已报名的竞赛', blank=True, related_name='signed_contests')
    finished_contests = models.ManyToManyField(Contest, verbose_name='已完成的竞赛', blank=True, related_name='finished_contests')

    class Meta:
        verbose_name = '普通用户（user）'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
