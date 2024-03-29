from django.db.models.signals import post_save
from .models import User, DoctorProfile, DoctorAvailability, PatientProfile
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'doctor':
            DoctorProfile.objects.create(doctor=instance)
        if instance.user_type == 'patient':
            PatientProfile.objects.create(patient=instance)

# @receiver(post_save, sender=User)
# def save_doctor_profile(sender, instance, **kwargs):
#     breakpoint()
#     if hasattr(instance, 'doctorprofile'):
#         instance.doctorprofile.save()
    

@receiver(post_save, sender=DoctorProfile)
def create_doctor_availability(sender, instance, created, **kwargs):
    if created:
        DoctorAvailability.objects.create(doctor_profile=instance)