from django import forms
from .models import Appointment
from accounts.models import User, DoctorProfile, DoctorAvailability, WorkingShift
import datetime as dt

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
# HOUR_CHOICES = WorkingShift.objects.filter(doctor_profile=)

class CreateAppointmentForm(forms.Form):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='doctor'),
        widget=forms.Select(attrs={'style': 'width: 500px;padding: 8px; margin-right: 16px;'}))

    # def __init__(self, doctor_id, *args,**kwargs):
    #     # doctor_id = kwargs.pop('doctor_id')
    #     super().__init__(*args,**kwargs)
    #     doctor = User.objects.get(id=doctor_id)
    #     self.fields['doctor'] = forms.CharField(widget=forms.TextInput(attrs={'value':doctor.get_full_name, 'readonly':True}))
    #     # self.fields['doctor'].widget = forms.TextInput(attrs={'value': doctor.get_full_name})

    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    appointment_time = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 200px;padding: 8px; margin-right: 16px;'}), choices = HOUR_CHOICES)
    reason = forms.CharField(max_length=254)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":8, "cols":20}))
        # class Meta:
        #     model = Appointment
        #     exclude = ['patient']

class DoctorAvailabilityForm(forms.Form):
    doctor = forms.ModelChoiceField(
    queryset=User.objects.filter(user_type='doctor').order_by(),
    widget=forms.Select(attrs={'style': 'width: 500px;padding: 8px; margin-right: 16px;'}))