# Generated by Django 3.2 on 2021-04-23 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_participant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competitionorganizer',
            options={'verbose_name': '竞赛发布者（user）', 'verbose_name_plural': '竞赛发布者（user）'},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': '普通用户（user）', 'verbose_name_plural': '普通用户（user）'},
        ),
        migrations.AlterModelOptions(
            name='problem',
            options={'ordering': ['-create_date'], 'verbose_name': '列题（problem）', 'verbose_name_plural': '列题（problem）'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户大类（user）', 'verbose_name_plural': '用户大类（user）'},
        ),
        migrations.AlterField(
            model_name='problem',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='题号'),
        ),
    ]
