# Generated by Django 4.0.1 on 2022-02-23 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_doctorprofile_nmc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='address_city',
            field=models.CharField(default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='address_street',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]