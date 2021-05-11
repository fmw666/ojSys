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
    def aplusb(self, a, b):
        # write your code here
        '''
    test_str = '''inputs = [[1,2],[100,200],[-3,-1],[0,3]]
corrects= [3,300,-4,3]

if len(inputs) != len(corrects):
    raise Exception('题目测试集错误，请联系管理员进行重修审核')

s = Solution()
for i in range(len(inputs)):
    params = inputs[i]
    if s.aplusb(params[0], params[1]) != corrects[i]:
        raise Exception('输入值:{0}, {1}. 不等于正确值:{2}'.format(params[0],params[1],corrects[i]))
'''

    id = models.BigAutoField(verbose_name='题号', primary_key=True)
    name = models.CharField(verbose_name='题目名称', max_length=100)
    message = models.TextField(verbose_name='题目描述信息', blank=False)
    input_example = models.TextField(verbose_name='输入样例', blank=True)
    output_example = models.TextField(verbose_name='输出样例', blank=True)
    challenge = models.TextField(verbose_name='挑战', blank=True)

    alg_type = models.CharField(verbose_name='算法类型', max_length=1, choices=ALG_CHOICES, default='b')
    ds_type = models.CharField(verbose_name='数据结构类型', max_length=1, choices=DS_CHOICES, default='b')

    header = models.CharField(verbose_name='难度', max_length=1, choices=HEADER_CHOICES, default='a')

    author = models.ForeignKey(User, verbose_name='题目作者', on_delete=models.DO_NOTHING, related_name='题目作者')
    public = models.BooleanField(default=True, verbose_name='是否公开')

    init_code = models.TextField(verbose_name='题目初始化显示', default=init_str)
    test_code = models.TextField(verbose_name='题目测试代码文本部分', default=test_str)

    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)

    def __str__(self):
        return '{0}. {1}'.format(self.id, self.name)

    class Meta:
        ordering = ['-create_date']
        verbose_name = '列题（problem）'
        verbose_name_plural = verbose_name


