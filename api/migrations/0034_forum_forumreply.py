# Generated by Django 3.2 on 2021-05-06 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_alter_contest_sign_up_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='帖子标题')),
                ('content', models.TextField(default='', verbose_name='帖子内容')),
                ('publish_date', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('modified', models.BooleanField(default=False, verbose_name='是否修改过')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='forum_author', to=settings.AUTH_USER_MODEL, verbose_name='帖子作者')),
            ],
            options={
                'verbose_name': '论坛（forum）',
                'verbose_name_plural': '论坛（forum）',
                'ordering': ['-publish_date', '-modify_date', '-author'],
            },
        ),
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', verbose_name='回复内容')),
                ('publish_date', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reply_author', to=settings.AUTH_USER_MODEL, verbose_name='回复作者')),
                ('fid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='api.forum', verbose_name='回复论坛id')),
            ],
        ),
    ]