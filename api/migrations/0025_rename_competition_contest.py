# Generated by Django 3.2 on 2021-05-04 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20210505_0531'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Competition',
            new_name='Contest',
        ),
    ]
