from django.contrib.auth.forms import UserCreationForm
from .models import User, DoctorAvailability, WorkingShift
from django import forms
from django.forms import ModelForm, fields
import datetime as dt
from entangled.forms import EntangledModelForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username','first_name', 'middle_name', 'last_name','user_type']

DAY_CHOICES = (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

# class DoctorAvailabilityForm(forms.Form):
#     available_days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices = DAY_CHOICES)
#     available_start_time = forms.ChoiceField(widget=forms.Select(), choices = HOUR_CHOICES)
#     available_end_time = forms.ChoiceField(widget=forms.Select(), choices = HOUR_CHOICES)

# class DoctorAvailabilityForm(EntangledModelForm):
#     days= fields.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=DAY_CHOICES)
#     start_time = fields.ChoiceField(choices = HOUR_CHOICES)
#     end_time = fields.ChoiceField(choices = HOUR_CHOICES)

#     class Meta:
#         model = DoctorAvailability
#         entangled_fields = {'working_shifts': ['days', 'start_time', 'end_time']}
#         untangled_fields = ['doctor','available_status']
#         exclude = ['doctor','available_status']

class DoctorWorkingShiftForm(forms.Form):
    working_day = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 200px;padding: 8px; margin-right: 16px;'}), choices = DAY_CHOICES)
    start_time = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 200px;padding: 8px; margin-right: 16px;'}), choices = HOUR_CHOICES)
    end_time = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 200px;padding: 8px; margin-right: 16px;'}), choices = HOUR_CHOICES)
    
    # class Meta:
    #     model = WorkingShift
    #     exclude = ['doctor_profile']
    #     widget = {
    #         'start_time': forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices = DAY_CHOICES)
    #     }