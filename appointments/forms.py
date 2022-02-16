from django import forms
from .models import Appointment
from accounts.models import User, DoctorProfile, DoctorAvailability
import datetime as dt

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

class CreateAppointmentForm(forms.Form):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='doctor'),
        widget=forms.Select(attrs={'style': 'width: 500px;padding: 8px; margin-right: 16px;'}))
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