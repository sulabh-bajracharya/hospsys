# Generated by Django 4.0.1 on 2022-02-10 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_doctorprofile_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='address_city',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='address_street',
            field=models.CharField(default='', max_length=255),
        ),
    ]
