import os
import sys
import subprocess
import tempfile
import time

# 创建临时文件夹,返回临时文件夹路径
TempFile = tempfile.mkdtemp(suffix='_test', prefix='python_')
# 文件名
FileNum = int(time.time() * 1000)
# python编译器位置
EXEC = sys.executable


# 获取python版本
def get_version():
    v = sys.version_info
    version = "python %s.%s" % (v.major, v.minor)
    return version


# 获得py文件名
def get_py_name():
    global FileNum
    return 'test_%d' % FileNum


# 接收代码写入文件
def write_file(py_name, p_code):
    f_path = os.path.join(TempFile, '%s.py' % py_name)
    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(p_code)
    print('file path: %s' % f_path)
    return f_path


# 编码
def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')


# 主执行函数
def run(p_code):
    r = dict()
    r["version"] = get_version()
    py_name = get_py_name()
    f_path = write_file(py_name, p_code)
    try:
        # subprocess.check_output 是 父进程等待子进程完成，返回子进程向标准输出的输出结果
        # stderr是标准输出的类型
        out_data = decode(subprocess.check_output(
            [EXEC, f_path], stderr=subprocess.STDOUT, timeout=5))
    except subprocess.CalledProcessError as e:
        # e.output是错误信息标准输出
        # 错误返回的数据
        r["code"] = 'wa'
        r["output"] = decode(e.output)
        return r
    else:
        # 成功返回的数据
        r['output'] = out_data
        r["code"] = "ac"
        return r
    finally:
        # 删除文件(其实不用删除临时文件会自动删除)
        try:
            os.remove(f_path)
        except FileNotFoundError as e:
            print(e)
            exit(1)


if __name__ == '__main__':
    code = """
class Solution:
    '''
    @param: n: An integer
    @return: An integer, denote the number of trailing zeros in n!
    '''
    def trailingZeros(self, n):
        # write your code here, try to do it without arithmetic operators.
        sum = 0
        while(n):
            sum += n // 5
            n //= 5
        return sum

s = Solution()
for _ in range(3):
    assert s.trailingZeros(11) == 2
"""

    # {'version': 'python 3.9', 'output': '2\r\n', 'code': 'ac'}
    print(run(code))
