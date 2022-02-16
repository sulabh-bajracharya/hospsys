from django.db import models
from accounts.models import User

# Create your models here.
class Appointment(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('deleted', 'Deleted')
    ]
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='appointment_doctor', limit_choices_to={'user_type':'doctor'})
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='appointment_patient', limit_choices_to={'user_type':'patient'})
    appointment_date = models.DateField(auto_now=False, auto_now_add=False)
    appointment_time = models.TimeField(auto_now=False, auto_now_add=False)
    reason = models.CharField(max_length=254)
    description = models.TextField(null=True)
    approval_status = models.CharField(max_length=10, choices = APPROVAL_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.reason
