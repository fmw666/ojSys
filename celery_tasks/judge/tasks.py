from celery_tasks.main import celery_app
from subprocess import call, CREATE_NO_WINDOW
import os


@celery_app.task(name='celery_tasks.judge.tasks.judge_code')
def judge_code(user_id, code_id, code):
    """
    运算代码
    :param user_id: 执行人
    :param code_id: 代码题号
    :param code: 代码
    :return:
    """
    # celery_tasks/judge/questions/1
    path = os.path.join(os.getcwd(), 'celery_tasks', 'judge', 'questions', code_id)

    # tmp + user_id  celery_tasks/judge/questions/1/tmp_2.py
    program_to_test = os.path.join(path, 'tmp_{}.py'.format(user_id))
    code_text = '''while True:
    line = input()
    if not line:
        break
    line = sum([int(num) for num in line.split(',')])
    print(line)
    '''
    # print(code)
    with open(program_to_test, 'w') as fp:
        fp.write(code)

    error_path = os.path.join(path, 'error_{}.txt'.format(user_id))
    output_path = os.path.join(path, 'out_{}.txt'.format(user_id))

    call(f'python {program_to_test}',  # 执行被测程序
         stdin=open(os.path.join(path, 'in.txt')),  # 指定输入源
         stderr=open(error_path, 'w'),  # 指定错误输出
         stdout=open(output_path, 'w'),  # 指定结果输出
         timeout=10,  # 10 秒没执行完就强制结束
         creationflags=CREATE_NO_WINDOW)  # 不创建 CMD 窗口

    # 读取被测程序生成的结果文件
    out1, out2 = '', ''
    with open(output_path) as fp1, open(os.path.join(path, 'current_output.txt')) as fp2:
        out1, out2 = fp1.readlines(), fp2.readlines()

    try:
        os.remove(program_to_test)
    except FileNotFoundError:
        pass

    if out1 != out2:
        return 0
    return 1

    # with open('error.txt') as fp:
    #     content = fp.readlines()
    # if content:
    #     print('程序语法错误，详情如下：\n', *content)
