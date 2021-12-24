# Generated by Django 2.2.5 on 2021-12-16 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('user', '0002_auto_20211216_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False, verbose_name='任务id')),
                ('task_info', models.CharField(default='', max_length=80, verbose_name='任务描述')),
            ],
            options={
                'db_table': 'Task',
            },
        ),
        migrations.CreateModel(
            name='TaskDistribution',
            fields=[
                ('task_distribution_id', models.AutoField(primary_key=True, serialize=False, verbose_name='分配任务id')),
                ('task_distribution_state', models.CharField(default='', max_length=20, verbose_name='分配任务状态')),
                ('task_distribution_is_accepted', models.CharField(default='', max_length=6, verbose_name='分配任务是否被接收')),
                ('task_distribution_begin_time', models.CharField(default='', max_length=20, verbose_name='分配任务开始时间')),
                ('task_distribution_endline', models.CharField(default='', max_length=20, verbose_name='分配任务结束时间')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Manager')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Staff')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='task.Task')),
            ],
            options={
                'db_table': 'TaskDistribution',
            },
        ),
        migrations.CreateModel(
            name='TaskAdvise',
            fields=[
                ('task_advise_id', models.AutoField(primary_key=True, serialize=False, verbose_name='任务审核id')),
                ('task_advise_content', models.CharField(default='', max_length=100, verbose_name='任务审核建议')),
                ('task_reviewer', models.CharField(default='', max_length=20, verbose_name='任务审核人')),
                ('task_distribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.TaskDistribution')),
            ],
            options={
                'db_table': 'TaskAdvise',
            },
        ),
    ]