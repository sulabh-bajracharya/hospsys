# Generated by Django 4.0.1 on 2022-01-26 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('reason', models.CharField(max_length=254)),
                ('description', models.TextField(null=True)),
                ('doctor', models.ForeignKey(limit_choices_to={'user_type': 'doctor'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointment_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(limit_choices_to={'user_type': 'patient'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointment_patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
