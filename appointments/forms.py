from django import forms
from .models import Appointment
from accounts.models import WorkingShift, User, DoctorProfile
from accounts.models import User, DoctorProfile, DoctorAvailability, WorkingShift
import datetime as dt

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

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

# doctor_profile = DoctorProfile.objects.get(doctor=User.objects.get(pk=request.session.pop('doctor_id')))
# HOUR_CHOICES = WorkingShift.objects.filter(doctor_profile=doctor_profile)

class CreateAppointmentForm(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     working_shifts = kwargs.pop('working_shifts', None)
    #     working_days = []
    #     for shifts in working_shifts:
    #         working_days.append(shifts.working_day)
    #     super(CreateAppointmentForm, self).__init__(*args, **kwargs)
        # working_shifts = WorkingShift.objects.filter(doctor_profile = instance.doctorprofile)
        # self.fields['appointment_date'].widget = forms.Select(choices=working_days)
        # self.fields['appointment_time'].queryset = working_shifts


    # appointment_date = forms.ModelChoiceField(queryset=WorkingShift.objects.all())
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    preferred_appointment_time = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 200px;padding: 8px; margin-right: 16px;'}), choices = TIMESLOT_LIST)
    reason = forms.CharField(max_length=254)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":8, "cols":20}))
       

class DoctorAvailabilityForm(forms.Form):
    doctor = forms.ModelChoiceField(
    queryset=User.objects.filter(user_type='doctor').order_by(),
    widget=forms.Select(attrs={'style': 'width: 500px;padding: 8px; margin-right: 16px;'}))

class EditAppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    appointment_time = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 200px;padding: 8px; margin-right: 16px;'}), choices = TIMESLOT_LIST)
    reason = forms.CharField(max_length=254)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":8, "cols":20}))

    class Meta:
        model = Appointment
        fields = ['appointment_date','appointment_time', 'reason','description']

