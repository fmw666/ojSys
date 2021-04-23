from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Problem(models.Model):
    ALG_CHOICES = (
        ('b', '基础'),
        ('g', '贪心算法')
    )
    DS_CHOICES = (
        ('b', '基础'),
        ('a', '数组')
    )

    id = models.IntegerField(verbose_name='题号', primary_key=True)
    name = models.CharField(verbose_name='题目名称', max_length=100)
    message = models.TextField(verbose_name='题目描述信息', blank=False)

    alg_type = models.CharField(verbose_name='算法类型', max_length=1, choices=ALG_CHOICES, default='b')
    ds_type = models.CharField(verbose_name='数据结构类型', max_length=1, choices=DS_CHOICES, default='b')

    author = models.ForeignKey(User, verbose_name='题目作者', on_delete=models.DO_NOTHING, related_name='题目作者')
    inputs = models.TextField(verbose_name='题目输入流', null=True, blank=True)
    correct_outs = models.TextField(verbose_name='题目正确输入信息')
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)

    def __str__(self):
        return '{0}. {1}'.format(self.id, self.name)

    class Meta:
        ordering = ['-create_date']
        verbose_name = '列题（problem）'
        verbose_name_plural = verbose_name


