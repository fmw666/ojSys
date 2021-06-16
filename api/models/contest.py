# utils
import datetime

# django
from django.utils import timezone
from django.db import models

# models
from .problem import Problem
from .user.organizer import Organizer
from .user.user import User


class Contest(models.Model):

    name = models.CharField(verbose_name='比赛名称', max_length=100)
    message = models.TextField(verbose_name='比赛描述信息', blank=False, default='')
    reward = models.TextField(verbose_name='比赛奖励信息', blank=False, default='')
    requirement = models.TextField(verbose_name='比赛要求信息', blank=True)
    problems = models.ManyToManyField(Problem)

    author = models.ForeignKey(Organizer, verbose_name='机构', on_delete=models.CASCADE, related_name='出题方')
    sign_up_start_date = models.DateTimeField(verbose_name='报名开始时间', help_text='Format is: yyyy-mm-dd hh:mm',
                                              blank=False, default=timezone.now)
    sign_up_end_date = models.DateTimeField(verbose_name='报名结束时间', help_text='Format is: yyyy-mm-dd hh:mm',
                                            blank=False, default=timezone.now)
    contest_start_date = models.DateTimeField(verbose_name='比赛开始时间', help_text='Format is: yyyy-mm-dd hh:mm',
                                              blank=False, default=timezone.now)
    contest_end_date = models.DateTimeField(verbose_name='比赛结束时间', help_text='Format is: yyyy-mm-dd hh:mm',
                                            blank=False, default=timezone.now)

    is_no = models.BooleanField(verbose_name='未开始', default=True)
    is_sign = models.BooleanField(verbose_name='报名中', default=False)
    is_wait = models.BooleanField(verbose_name='等待中', default=False)
    is_start = models.BooleanField(verbose_name='已开始', default=False)
    is_end = models.BooleanField(verbose_name='已结束', default=False)

    # 报名的人
    sign_up_user = models.ManyToManyField(User, verbose_name='报名的人', blank=True, related_name='sign_up')
    # 提交的人
    commit_user = models.ManyToManyField(User, verbose_name='提交的人', blank=True, related_name='commit')

    def clean(self, *args, **kwargs):
        # run the base validation
        super(Contest, self).clean()

        # Don't allow dates older than now.
        if self.sign_up_start_date < datetime.datetime.now():
            self.sign_up_start_date = datetime.datetime.now()
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


# 比赛结果信息表
class ContestInfoResult(models.Model):
    contest = models.ForeignKey(Contest, related_name='contest_info', on_delete=models.CASCADE, verbose_name='比赛题目')
    user = models.ForeignKey(User, related_name='user_info', on_delete=models.CASCADE, verbose_name='比赛参与用户')
    pass_problems = models.ManyToManyField(Problem, verbose_name='用户完成题目')
    spend_time = models.CharField(max_length=20, help_text='format as: 5h3m53s', default='0h0m0s')
    ranking = models.IntegerField(unique=False, blank=True, verbose_name='用户排名', default=0)

    def __str__(self):
        return 'user: {0} in contest: {1}. pass_problems: {2}, ranking: {3}'\
            .format(self.user.username, self.contest.name, self.pass_problems, self.ranking)

    class Meta:
        verbose_name = '比赛-用户-信息记录（Contest Info Result）'
        verbose_name_plural = verbose_name
