# Generated by Django 3.2 on 2021-05-10 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20210510_1614'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestinforesult',
            options={'verbose_name': '比赛-用户-信息记录（Contest Info Result）', 'verbose_name_plural': '比赛-用户-信息记录（Contest Info Result）'},
        ),
        migrations.AddField(
            model_name='contestinforesult',
            name='ranking',
            field=models.IntegerField(blank=True, default=0, verbose_name='用户排名'),
        ),
        migrations.DeleteModel(
            name='ContestRankingResult',
        ),
    ]
