# Generated by Django 3.2 on 2021-04-23 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210423_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='id',
        ),
        migrations.AddField(
            model_name='participant',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
