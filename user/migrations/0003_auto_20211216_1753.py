# Generated by Django 2.2.5 on 2021-12-16 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20211216_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='job',
            field=models.CharField(default='模型员工', max_length=30, verbose_name='职务'),
        ),
    ]
