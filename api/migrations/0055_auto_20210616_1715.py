# Generated by Django 3.2.3 on 2021-06-16 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20210616_1714'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name': '用户-竞赛组织者（organizer）', 'verbose_name_plural': '用户-竞赛组织者（organizer）'},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': '用户-竞赛参与者（participant）', 'verbose_name_plural': '用户-竞赛参与者（participant）'},
        ),
    ]