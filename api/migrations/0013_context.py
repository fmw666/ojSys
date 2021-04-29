# Generated by Django 3.2 on 2021-04-26 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_problem_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='比赛名称')),
                ('message', models.TextField(verbose_name='比赛描述信息')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='出题方', to='api.participant', verbose_name='机构')),
                ('problems', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='题目', to='api.problem', verbose_name='题目')),
            ],
            options={
                'verbose_name': '比赛（context）',
                'verbose_name_plural': '比赛（context）',
                'ordering': ['-create_date'],
            },
        ),
    ]