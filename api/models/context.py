from django.db import models

from .problem import Problem
from .users import CompetitionOrganizer


class Context(models.Model):

    name = models.CharField(verbose_name='比赛名称', max_length=100)
    message = models.TextField(verbose_name='比赛描述信息', blank=False)
    problems = models.ManyToManyField(Problem)

    author = models.ForeignKey(CompetitionOrganizer, verbose_name='机构', on_delete=models.CASCADE, related_name='出题方')
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)

    def __str__(self):
        return '{0}. {1}'.format(self.name, self.author.user.username)

    class Meta:
        ordering = ['-create_date']
        verbose_name = '比赛（context）'
        verbose_name_plural = verbose_name


