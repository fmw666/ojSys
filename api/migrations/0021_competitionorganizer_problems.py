# Generated by Django 3.2 on 2021-04-30 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_participant_solved_problems'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionorganizer',
            name='problems',
            field=models.ManyToManyField(blank=True, to='api.Problem', verbose_name='面试题'),
        ),
    ]
