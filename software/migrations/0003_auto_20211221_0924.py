# Generated by Django 2.2.5 on 2021-12-21 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0002_auto_20211218_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('software_id', models.AutoField(primary_key=True, serialize=False, verbose_name='软甲id')),
                ('software_name', models.CharField(default='', max_length=20, verbose_name='软件名字')),
                ('software_property', models.CharField(default='', max_length=20, verbose_name='软件性质')),
            ],
            options={
                'db_table': 'Software',
            },
        ),
        migrations.RemoveField(
            model_name='staffusingsoftwarerecord',
            name='software_name',
        ),
        migrations.RemoveField(
            model_name='staffusingsoftwarerecord',
            name='software_property',
        ),
        migrations.AddField(
            model_name='staffusingsoftwarerecord',
            name='software_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='software.Software'),
        ),
    ]