# Generated by Django 3.2 on 2021-05-04 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_competitionorganizer_problems'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='challenge',
            field=models.TextField(blank=True, verbose_name='挑战'),
        ),
        migrations.AddField(
            model_name='problem',
            name='input_example',
            field=models.TextField(blank=True, verbose_name='输入样例'),
        ),
        migrations.AddField(
            model_name='problem',
            name='output_example',
            field=models.TextField(blank=True, verbose_name='输出样例'),
        ),
    ]
