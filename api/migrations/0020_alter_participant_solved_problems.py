# Generated by Django 3.2 on 2021-04-28 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20210428_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='solved_problems',
            field=models.ManyToManyField(blank=True, to='api.Problem', verbose_name='已解决的题'),
        ),
    ]
