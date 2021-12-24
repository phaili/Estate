# Generated by Django 2.2.5 on 2021-12-16 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False, verbose_name='客户id')),
                ('client_name', models.CharField(default='', max_length=20, verbose_name='客户姓名')),
                ('client_phone', models.CharField(default='', max_length=20, verbose_name='客户电话')),
                ('client_qq', models.CharField(default='', max_length=14, verbose_name='客户qq')),
                ('client_email', models.CharField(default='', max_length=20, verbose_name='客户邮箱')),
            ],
            options={
                'db_table': 'Client',
            },
        ),
    ]
