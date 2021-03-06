# Generated by Django 2.2.5 on 2021-12-16 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False, verbose_name='项目id')),
                ('project_name', models.CharField(default='', max_length=30, verbose_name='项目名字')),
                ('project_schedule', models.CharField(default='', max_length=10, verbose_name='项目进度')),
                ('project_price', models.CharField(default='', max_length=10, verbose_name='项目报价')),
                ('project_beg_time', models.CharField(default='', max_length=20, verbose_name='项目开始时间')),
                ('project_person_in_charge', models.CharField(default='', max_length=20, verbose_name='项目负责人')),
                ('project_state', models.CharField(default='', max_length=10, verbose_name='项目状态')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='client.Client')),
            ],
            options={
                'db_table': 'Project',
            },
        ),
    ]
