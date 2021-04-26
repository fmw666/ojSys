# Generated by Django 3.2 on 2021-04-26 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_context'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='context',
            name='problems',
        ),
        migrations.AddField(
            model_name='context',
            name='problems',
            field=models.ManyToManyField(to='api.Problem'),
        ),
    ]
