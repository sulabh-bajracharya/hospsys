from django.db import models
from accounts.models import User

# Create your models here.
class Appointment(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('deleted', 'Deleted'),
        ('cancelled', 'Cancelled'),
    ]

    TIMESLOT_LIST = (
        (0, '09:00 - 09:30'),
        (1, '09:30 - 10:00'),
        (2, '10:00 - 10:30'),
        (3, '10:30 - 11:00'),
        (4, '11:00 - 11:30'),
        (5, '11:30 - 12:00'),
        (6, '12:00 - 12:30'),
        (7, '12:30 - 13:00'),
        (8, '13:00 - 13:30'),
        (9, '13:30 - 14:00'),
        (10, '14:00 - 14:30'),
        (11, '14:30 - 15:00'),
        (12, '15:00 - 15:30'),
        (13, '15:30 - 16:00'),
        (14, '16:00 - 16:30'),
        (15, '16:30 - 17:00'),
        (16, '17:00 - 17:30'),
    )

    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='appointment_doctor', limit_choices_to={'user_type':'doctor'})
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='appointment_patient', limit_choices_to={'user_type':'patient'})
    appointment_date = models.DateField(auto_now=False, auto_now_add=False)
    appointment_time = models.IntegerField(default=100, choices=TIMESLOT_LIST)
    reason = models.CharField(max_length=254)
    description = models.TextField(null=True)
    approval_status = models.CharField(max_length=10, choices = APPROVAL_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.reason

    @property
    def timeslot(self):
        return self.TIMESLOT_LIST[self.appointment_time][1]
