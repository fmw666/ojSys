"""
总配置文件，包含前后端配置

注，实际版本中，EMAIL_HOST 和 SMS_CONFIG 必须手动配置！
"""


# redis 服务器地址
REDIS_SERVER = '127.0.0.1:6379'

# mysql 配置
MYSQL_CONFIG = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'USER': 'admin',
    'PASSWORD': 'admin',
    'NAME': 'oj_sys'
}

# 前台 URL
FRONT_URL = 'http://127.0.0.1:3000'

# 邮箱服务器配置
EMAIL_HOST = {
    'USER': '784958034@qq.com',
    'PASSWORD': 'cpsongpnazokbbfb'
}

# 容联云短信服务配置
SMS_CONFIG = {
    'accId': '8a216da878005a8001782111e32e0cb5',
    'accToken': '73464666c177436e9fffbf821aebf443',
    'appId': '8a216da878005a8001782111e4070cbc'
}