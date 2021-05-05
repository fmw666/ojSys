1、下载 node.js，并导入环境变量
2、下载Python、Pycharm、VSCode
3、下载mysql、redis

mysql下载地址：https://dev.mysql.com/downloads/file/?id=501541
redis下载地址：https://github.com/MicrosoftArchive/redis/releases

导入mysql环境变量
进入mysql：mysql -uroot -padmin
创建表：create database oj_sys default charset=utf8;
创建数据库用户
create user admin identified by 'admin';
grant all on oj_sys.* to 'admin'@'%';
flush privileges;

python 依赖包见 requirements.txt

启动 mysql，在服务开启 mysql，如果没有就先执行 mysqld install
启动 redis，在其安装目录下
redis-server --service-install redis.windows-service.conf --loglevel verbose
redis-server --service-start

1、开启异步定时：
celery -A celery_tasks.main beat -l info
2、开启异步任务：
celery -A celery_tasks.main worker -l info