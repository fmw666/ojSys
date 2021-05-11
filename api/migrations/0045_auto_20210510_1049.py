# Generated by Django 3.2 on 2021-05-10 10:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20210510_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contest_end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Format is: yyyy-mm-dd hh:mm', verbose_name='比赛结束时间'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='contest_start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Format is: yyyy-mm-dd hh:mm', verbose_name='比赛开始时间'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='sign_up_end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Format is: yyyy-mm-dd hh:mm', verbose_name='报名结束时间'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='sign_up_start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Format is: yyyy-mm-dd hh:mm', verbose_name='报名开始时间'),
        ),
    ]