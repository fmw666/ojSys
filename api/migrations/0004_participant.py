# Generated by Django 3.2 on 2021-04-23 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_problem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved_problems', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='已解决的题', to='api.problem', verbose_name='已解决的题')),
            ],
        ),
    ]
