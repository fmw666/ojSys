from celery_tasks.main import celery_app

from celery_tasks.judge.compiler import run


@celery_app.task(name='celery_tasks.judge.tasks.judge_code')
def judge_code(code, data_in, data_cor_output):
    """
    运算代码
    :param code: 代码
    :param data_in: 代码测试输入
    :param data_cor_output: 代码正确输出
    :return:
    """
    # 构建测试数据
    data_in_lst = data_in.strip().split('\r\n')
    data_in_str = '['
    for dil in data_in_lst:
        data_in_str += dil + ','
    data_in_str = data_in_str[:-1]
    data_in_str += ']'

    data_cor_output_lst = data_cor_output.strip().split('\r\n')
    data_cor_output_str = '['
    for dil in data_cor_output_lst:
        data_cor_output_str += dil + ','
    data_cor_output_str = data_cor_output_str[:-1]
    data_cor_output_str += ']'

    test_code = '''
data_in_lst = {0}
data_cor_output_lst = {1}

s = Solution()
for i in range(len(data_in_lst)):
    assert s.function(data_in_lst[i]) == data_cor_output_lst[i]
'''.format(data_in_str, data_cor_output_str)


    # 执行
    return run(code + '\r\n' + test_code)

