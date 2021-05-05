import datetime

import pytz
from django.db import models

from .problem import Problem
from .user.contestorganizer import ContestOrganizer


class Contest(models.Model):

    name = models.CharField(verbose_name='比赛名称', max_length=100)
    message = models.TextField(verbose_name='比赛描述信息', blank=False, default='')
    reward = models.TextField(verbose_name='比赛奖励信息', blank=False, default='')
    requirement = models.TextField(verbose_name='比赛要求信息', blank=True)
    problems = models.ManyToManyField(Problem)

    author = models.ForeignKey(ContestOrganizer, verbose_name='机构', on_delete=models.CASCADE, related_name='出题方')
    sign_up_start_date = models.DateTimeField(verbose_name='报名开始时间', help_text='Format is: yyyy-mm-dd hh:mm')
    sign_up_end_date = models.DateTimeField(verbose_name='报名结束时间', help_text='Format is: yyyy-mm-dd hh:mm')
    contest_start_date = models.DateTimeField(verbose_name='比赛开始时间', help_text='Format is: yyyy-mm-dd hh:mm')
    contest_end_date = models.DateTimeField(verbose_name='比赛结束时间', help_text='Format is: yyyy-mm-dd hh:mm')

    is_no = models.BooleanField(verbose_name='未开始', default=True)
    is_sign = models.BooleanField(verbose_name='报名中', default=False)
    is_start = models.BooleanField(verbose_name='已开始', default=False)
    is_end = models.BooleanField(verbose_name='已结束', default=False)

    def clean(self, *args, **kwargs):
        # run the base validation
        super(Contest, self).clean()

        # Don't allow dates older than now.
        if self.sign_up_start_date < datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')):
            self.sign_up_start_date = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
        if self.sign_up_end_date < self.sign_up_start_date:
            self.sign_up_end_date = self.sign_up_start_date
        if self.contest_start_date < self.sign_up_end_date:
            self.contest_start_date = self.sign_up_end_date
        if self.contest_end_date < self.contest_start_date:
            self.contest_end_date = self.contest_start_date

    def __str__(self):
        return '{0}. {1}'.format(self.name, self.author.user.username)

    class Meta:
        ordering = ['-sign_up_start_date', '-sign_up_end_date', '-contest_start_date', '-contest_end_date']
        verbose_name = '比赛（contest）'
        verbose_name_plural = verbose_name


