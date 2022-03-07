from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone
from django.contrib.postgres.fields import ArrayField
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
    )
    middle_name =  models.CharField(blank=True, max_length=150, verbose_name='middle name')
    email = models.EmailField(max_length=254, verbose_name='email address', unique=True)
    user_type = models.CharField(choices = USER_TYPE_CHOICES, max_length=10, verbose_name='user type')
    profile_image = CloudinaryField('profile_image', null=True, blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='updated at')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']    

    def __str__(self):
        return self.email

    @property
    def is_patient(self):
        if self.user_type == 'patient':
            return True
        else:
            return False

    @property
    def is_doctor(self):
        if self.user_type == 'doctor':
            return True
        else:
            return False

class PatientProfile(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE,limit_choices_to={'user_type':'patient'}, null=True, related_name='patientprofile')
    address_street = models.CharField(max_length=255, default='', null=True)
    address_city = models.CharField(max_length=50, default='', null=True)
    # phone = models.CharField(max_length=15)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.patient.get_full_name().title() + '\'s Profile'

    def get_full_address(self):
        return self.address_street + ', ' + self.address_city

    def profile_incomplete(self):
        if self.address_street == None or self.address_city == None:
            return True
        else:
            return False

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type':'doctor'}, null=True, related_name='doctorprofile')
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    nmc = models.IntegerField(default=0, null=True)
    nmc_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.doctor.get_full_name().title() + '\'s Profile'

    def profile_incomplete(self):
        if self.department == None or self.nmc == None:
            return True
        else:
            return False

    def is_nmc_verified(self):
        if self.nmc_verified:
            return True
        else:
            return False

class DoctorAvailability(models.Model):
    STATUS_CHOICES = [
        ('online','Online'),
        ('offline','Offline'),
    ]

    doctor_profile = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE)
    # working_days = ArrayField(models.CharField(max_length=20, choices=DAYS_CHOICES, null=True))
    # working_shifts = models.JSONField(null=False, default=dict)
    # available_days = ArrayField(models.CharField(max_length=20, choices=DAYS_CHOICES, null=True))
    # available_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    # available_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    available_status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='offline')

class WorkingShift(models.Model):
    DAYS_CHOICES = [
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    working_day = models.CharField(max_length=20, choices=DAYS_CHOICES)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    # class Meta:
        # unique_together = ['doctor_profile','working_day']