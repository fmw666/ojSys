# 敲哈儿码都（kk-code） 💫

> 本篇内容：介绍本项目主要内容，并将指导您完成对项目的启动

<div align="right">
<p><i>请根据语言习惯选择对应文档：<br>Please select a doc for your language：</i><br>---&emsp;</p>

<p>中文版文档（正在浏览）<br>Chinese doc（reading now）</p>

<p>
  <a href="README-en.md">英文版文档（点击切换）</a>
  <br><a href="README-en.md">English doc（click for switching）</a>
</p>

</div>

**目录**

+ 🎉 **[项目介绍](#-项目介绍)**
+ 🎯 **[待办事件](#-待办事件)**
+ 💬 **[依赖和操作说明文档](#-依赖和操作说明文档)**
+ 🚀 **[项目启动](#-项目启动)**

<br>

## 🎉 项目介绍

### 项目名

- 中文名：敲哈儿码都
- 英文名：kk-code（knock a while code）

### 主要功能

- 算法刷题
- 参与比赛
- 论坛

### 开始日期

- 2021.4

### 开发团队

+ [fmw666](https://github.com/fmw666)

### 目录结构

```
ojSys
├── api
│   ├── readme.txt  # how to run？（介绍及运行说明）
│   ├── main.py     # main entrance（程序运行主入口）
│   ├── xxx.py      # assistant program（辅助程序，数量不定）
│   ├── assets      # 资源存放文件夹
│   │   ├── ...
├── celery_tasks
│   ├── readme.txt  # how to run？（介绍及运行说明）
│   ├── main.py     # main entrance（程序运行主入口）
│   ├── xxx.py      # assistant program（辅助程序，数量不定）
│   ├── assets      # 资源存放文件夹
│   │   ├── ...
├── client
├── server

├── .gitignore
├── README-en.md
├── README.md
├── manage.py
├── requirements.txt
```

## 🎯 待办事件

- [ ] Linux 版本同步
- [ ] Linux 下 crontab 定时任务开启
- [ ] 后台数据在 admin 中心导入导出
- [ ] 未登录无法查看报名比赛
- [ ] 帖子空验证
- [ ] auth 板块前端页面优化
- [ ] vue 路由设置 title
- [ ] 过滤条件放进 session 里，刷新不重置，关闭页面才重置

## 💬 依赖和操作说明文档

### 开发软件

1. 下载 node.js、Python3.6+，并导入环境变量（必须）
2. 下载 mysql、redis（必须）
3. 下载 Pycharm、VSCode（非必须）
4. python 依赖包见 requirements.txt（推荐使用虚拟环境）

> mysql下载地址：[https://dev.mysql.com/downloads/file/?id=501541](https://dev.mysql.com/downloads/file/?id=501541)

> redis下载地址：[https://github.com/MicrosoftArchive/redis/releases](https://github.com/MicrosoftArchive/redis/release)

### 配置 mysql

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
+ 启动mysql
  
  在服务开启 mysql，如果没有就先执行 mysqld install

### redis 启动

+ windows：
  
  在 redis 安装目录下
  
  ```cmd
  > redis-server --service-install redis.windows-service.conf --loglevel verbose
  > redis-server --service-start
  ```

### celery 说明

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

## 🚀 项目启动

+ 修改配置文件

  其它配置均可默认，但是 *邮箱服务器* 和 *容联云通讯* 必须写入配置

+ 开启控制台 1 —— drf

  ```bash
  # 项目根路径下
  ojSys > python manage.py runserver 8000
  ```

+ 开启控制台 2 —— celery

  ```bash
  # 项目根路径下
  ojSys > celery -A celery_tasks.main worker -l info
  ```

+ 开启控制台 3 —— vue

  ```bash
  # 项目根路径的 client 目录下
  ojSys/client > npm run serve
  ```
