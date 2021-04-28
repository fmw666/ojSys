from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Problem(models.Model):
    ALG_CHOICES = (
        ('b', '基础'),
        ('g', '贪心算法'),
        ('f', 'DFS/BFS'),
        ('x', '动态规划'),
        ('t', '二分法'),
        ('d', '最短路径算法')
    )
    DS_CHOICES = (
        ('b', '基础'),
        ('a', '数组'),
        ('l', '链表'),
        ('s', '栈'),
        ('q', '队列'),
        ('h', '哈希表'),
        ('t', '树'),
        ('p', '图')
    )
    HEADER_CHOICES = (
        ('a', '入门'),
        ('b', '简单'),
        ('c', '中等'),
        ('d', '困难'),
        ('e', '特难')
    )
    init_str = '''class Solution:
    """
    @param a: An integer
    @param b: An integer
    @return: The sum of a and b
    """
    def function(self, a, b):
        # write your code here
        '''
    test_str = '''
s = Solution()
for i in range(len(data_in_lst)):
    assert s.function(data_in_lst[i]) == data_cor_output_lst[i]
'''

    id = models.IntegerField(verbose_name='题号', primary_key=True)
    name = models.CharField(verbose_name='题目名称', max_length=100)
    message = models.TextField(verbose_name='题目描述信息', blank=False)

    alg_type = models.CharField(verbose_name='算法类型', max_length=1, choices=ALG_CHOICES, default='b')
    ds_type = models.CharField(verbose_name='数据结构类型', max_length=1, choices=DS_CHOICES, default='b')

    header = models.CharField(verbose_name='难度', max_length=1, choices=HEADER_CHOICES, default='a')

    author = models.ForeignKey(User, verbose_name='题目作者', on_delete=models.DO_NOTHING, related_name='题目作者')
    init_code = models.TextField(verbose_name='题目初始化显示', default=init_str)
    test_code = models.TextField(verbose_name='题目测试代码文本部分', default=test_str)

    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)

    def __str__(self):
        return '{0}. {1}'.format(self.id, self.name)

    class Meta:
        ordering = ['-create_date']
        verbose_name = '列题（problem）'
        verbose_name_plural = verbose_name


