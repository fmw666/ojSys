# Generated by Django 3.2 on 2021-05-11 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_alter_problem_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestinforesult',
            name='spend_time',
            field=models.CharField(default='0h0m0s', help_text='format as: 5h3m53s', max_length=20),
        ),
    ]
