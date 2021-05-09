from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Forum(models.Model):

    title = models.CharField(verbose_name='帖子标题', max_length=100)
    content = models.TextField(verbose_name='帖子内容', blank=False, default='')

    publish_date = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    modify_date = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)
    modified = models.BooleanField(verbose_name='是否修改过', default=False)

    like_cnt = models.ManyToManyField(User, verbose_name='点赞')
    author = models.ForeignKey(User, verbose_name='帖子作者', on_delete=models.DO_NOTHING, related_name='forum_author')

    def __str__(self):
        return '{0}. {1}'.format(self.title, self.author.username)

    class Meta:
        ordering = ['-publish_date', '-modify_date', '-author']
        verbose_name = '论坛（forum）'
        verbose_name_plural = verbose_name


class ForumReply(models.Model):
    content = models.TextField(verbose_name='回复内容', blank=False, default='')
    author = models.ForeignKey(User, verbose_name='回复作者', on_delete=models.DO_NOTHING, related_name='reply_author')

    publish_date = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    fid = models.ForeignKey(Forum, verbose_name='回复论坛id', on_delete=models.CASCADE, related_name='reply')

    def __str__(self):
        return '{0}. {1}'.format(self.fid, self.author.username)

    class Meta:
        ordering = ['-publish_date', '-fid', '-author']
        verbose_name = '论坛回复（reply）'
        verbose_name_plural = verbose_name
