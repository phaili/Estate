# Generated by Django 2.2.5 on 2021-12-18 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20211216_1753'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='manager',
            table='主管',
        ),
        migrations.AlterModelTable(
            name='staff',
            table='员工',
        ),
        migrations.AlterModelTable(
            name='staffevaluation',
            table='员工评价',
        ),
        migrations.AlterModelTable(
            name='staffturnover',
            table='员工流水',
        ),
    ]
