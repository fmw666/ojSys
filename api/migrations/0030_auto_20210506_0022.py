# Generated by Django 3.2.1 on 2021-05-05 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20210505_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='is_end',
            field=models.BooleanField(default=False, verbose_name='已结束'),
        ),
        migrations.AddField(
            model_name='contest',
            name='is_no',
            field=models.BooleanField(default=True, verbose_name='未开始'),
        ),
        migrations.AddField(
            model_name='contest',
            name='is_sign',
            field=models.BooleanField(default=False, verbose_name='报名中'),
        ),
        migrations.AddField(
            model_name='contest',
            name='is_start',
            field=models.BooleanField(default=False, verbose_name='已开始'),
        ),
    ]
