
# django
from django.db import models

# models
from .user import User
from ..problem import Problem


# 竞赛组织者
class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    problems = models.ManyToManyField(Problem, verbose_name='面试题', blank=True)

    class Meta:
        verbose_name = '用户-竞赛组织者（organizer）'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
