# Generated by Django 2.2.5 on 2021-12-18 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='client.Client'),
        ),
        migrations.AlterModelTable(
            name='project',
            table='项目',
        ),
    ]
