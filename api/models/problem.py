from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Problem(models.Model):
    name = models.CharField(verbose_name='题目名称', max_length=100)
    message = models.TextField(verbose_name='题目描述信息', blank=False)

    author = models.ForeignKey(User, verbose_name='题目作者', on_delete=models.DO_NOTHING, related_name='题目作者')
    inputs = models.TextField(verbose_name='题目输入流', null=True, blank=True)
    correct_outs = models.TextField(verbose_name='题目正确输入信息')
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_date']


