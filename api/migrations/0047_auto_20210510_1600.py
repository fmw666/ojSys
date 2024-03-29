# Generated by Django 3.2 on 2021-05-10 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_contest_is_wait'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='commit_user',
            field=models.ManyToManyField(blank=True, related_name='commit', to=settings.AUTH_USER_MODEL, verbose_name='提交的人'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='sign_up_user',
            field=models.ManyToManyField(blank=True, related_name='sign_up', to=settings.AUTH_USER_MODEL, verbose_name='报名的人'),
        ),
        migrations.CreateModel(
            name='ContestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.IntegerField(verbose_name='用户排名')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_result', to='api.contest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_result', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '比赛-用户-排名记录（Contest Result）',
                'verbose_name_plural': '比赛-用户-排名记录（Contest Result）',
                'ordering': ['-ranking'],
            },
        ),
    ]
