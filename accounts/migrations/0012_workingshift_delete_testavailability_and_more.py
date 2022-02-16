# Generated by Django 4.0.1 on 2022-01-27 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_rename_working_hours_doctoravailability_working_shifts'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkingShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_day', models.CharField(choices=[('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')], max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='TestAvailability',
        ),
        migrations.RemoveField(
            model_name='doctoravailability',
            name='working_shifts',
        ),
        migrations.AddField(
            model_name='workingshift',
            name='doctor_availability',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.doctoravailability'),
        ),
        migrations.AlterUniqueTogether(
            name='workingshift',
            unique_together={('doctor_availability', 'working_day')},
        ),
    ]
