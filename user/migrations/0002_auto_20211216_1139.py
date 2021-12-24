# Generated by Django 2.2.5 on 2021-12-16 03:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='staff',
            table='Staff',
        ),
        migrations.CreateModel(
            name='StaffTurnover',
            fields=[
                ('staff_turnover_id', models.AutoField(primary_key=True, serialize=False, verbose_name='员工流水id')),
                ('staff_turnover_basic_salary', models.CharField(default='', max_length=20, verbose_name='员工基础工资')),
                ('staff_turnover_deduction', models.CharField(default='', max_length=20, verbose_name='扣款')),
                ('staff_turnover_total', models.CharField(default='', max_length=20, verbose_name='总工资')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Staff')),
            ],
            options={
                'db_table': 'StaffTurnover',
            },
        ),
        migrations.CreateModel(
            name='StaffEvaluation',
            fields=[
                ('staff_evaluation_id', models.AutoField(primary_key=True, serialize=False, verbose_name='员工评估id')),
                ('staff_evaluation_info', models.CharField(default='', max_length=20, verbose_name='员工评估内容')),
                ('staff_evaluation_time', models.CharField(default='', max_length=20, verbose_name='员工评估记录时间')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Staff')),
            ],
            options={
                'db_table': 'StaffEvaluation',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('manager_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='主管工号')),
                ('manager_name', models.CharField(default='', max_length=20, verbose_name='主管姓名')),
                ('manager_phone', models.CharField(default='', max_length=20, verbose_name='主管电话')),
                ('manager_department', models.CharField(default='', max_length=20, verbose_name='主管所属部门')),
                ('manager_job', models.CharField(default='模型主管', max_length=20, verbose_name='主管职务')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_manager', models.ManyToManyField(to='project.Project')),
            ],
            options={
                'db_table': 'Manager',
            },
        ),
    ]