# Generated by Django 4.0.1 on 2022-01-26 17:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_doctorprofile_doctor_alter_user_user_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoravailability',
            name='available_days',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday')], default=['Sunday'], max_length=20), size=None),
        ),
    ]
