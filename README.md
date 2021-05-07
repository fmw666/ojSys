## 💬 依赖和操作说明文档

1. 下载 node.js，并导入环境变量

2. 下载Python、Pycharm、VSCode

3. 下载mysql、redis

> mysql下载地址：https://dev.mysql.com/downloads/file/?id=501541

> redis下载地址：https://github.com/MicrosoftArchive/redis/releases

### 导入mysql环境变量

+ 进入mysql：
  
    ```mysql
    $ mysql -uroot -padmin
    ```
  
+ 创建表：
  
    ```mysql
    mysql> create database oj_sys default charset=utf8;
    ```

+ 创建数据库用户：

    ```mysql
    mysql> create user admin identified by 'admin';
    mysql> grant all on oj_sys.* to 'admin'@'%';
    mysql> flush privileges;
    ```

python 依赖包见 requirements.txt

启动 mysql，在服务开启 mysql，如果没有就先执行 mysqld install
启动 redis，在其安装目录下
redis-server --service-install redis.windows-service.conf --loglevel verbose
redis-server --service-start

1. 发布异步任务：

    ```bash
    $ celery -A celery_tasks.main beat -l info
    ```

2. 开启异步任务：

    ```bash
    $ celery -A celery_tasks.main worker -l info
    ```

### Windows 定时任务

+ UrlCron Ver 1.0 Url定时请求器

    ```
    文件清单
  
    install.bat　 安装，将UrlCron服务安装到系统Servcie服务中，运行on.bat可马上执行
    on.bat　　　手动启动服务
    off.bat　　　手动停止服务
    uninstall.bat 卸载，从服务中删除UrlCron服务
    cron.log　　记录运行日志及请求错误记录
    -----------------------------------------------------
    cron.ini　　需要请求的URL清单配置，配置格式：时间(秒) 空格 Url地址，一行为一个任务线程
    ```