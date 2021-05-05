from django.db import models

from .user import User
from ..problem import Problem


# 竞赛发布者
class ContestOrganizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()

    problems = models.ManyToManyField(Problem, verbose_name='面试题', blank=True)

    class Meta:
        verbose_name = '竞赛发布者（user）'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
