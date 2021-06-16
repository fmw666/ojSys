# Generated by Django 3.2.3 on 2021-06-16 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20210616_1657'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContestOrganizer',
            new_name='Organizer',
        ),
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name': '竞赛组织者（organizer）', 'verbose_name_plural': '竞赛组织者（organizer）'},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': '竞赛参与者用户（participant）', 'verbose_name_plural': '竞赛参与者用户（participant）'},
        ),
    ]