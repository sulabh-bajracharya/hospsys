# Generated by Django 4.0.1 on 2022-01-27 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_workingshift_delete_testavailability_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingshift',
            name='doctor_availability',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.doctorprofile'),
        ),
    ]