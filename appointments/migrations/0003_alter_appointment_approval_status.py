# Generated by Django 4.0.1 on 2022-01-30 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_appointment_approval_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='approval_status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]