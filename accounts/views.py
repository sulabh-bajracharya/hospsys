from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, DoctorWorkingShiftForm
from django.urls import reverse
from .models import DoctorAvailability, DoctorProfile, WorkingShift
from django.views.generic.edit import UpdateView
from appointments.models import Appointment

# Create your views here.
def index(request):
    return HttpResponse("index page.")

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_doctor:
            working_shifts_form = DoctorWorkingShiftForm()
            appointments = Appointment.objects.filter(doctor = user)
            context = {
                'current_user': user,
                'working_shifts_form': working_shifts_form,
                'appointments': appointments,
            }
            return render(request, 'accounts/doctor_dashboard.html', context)
        elif user.is_patient:
            appointments = Appointment.objects.filter(patient = user)
            context = {
                'current_user': user,
                'appointments': appointments,
            }
            return render(request, 'accounts/patient_dashboard.html', context)
        else:
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        return HttpResponseRedirect(reverse('accounts:login'))

def view_working_shifts(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'doctor':
            working_shifts = WorkingShift.objects.filter(doctor_profile = request.user.doctorprofile)
            return render(request, 'accounts/view_availability.html', {'working_shifts': working_shifts})
        else:
            return HttpResponseRedirect(reverse('accounts:dashboard'))
    

# def change_availability(request):
#     if request.method == 'POST':
#         form = DoctorAvailabilityForm(request.POST)
#         available_days = []

#         if form.is_valid():
#             av_days = form.cleaned_data['available_days']
#             for av_day in av_days:
#                 available_days.append(av_day) 
#             available_start_time = form.cleaned_data['available_start_time']
#             available_end_time = form.cleaned_data['available_end_time']
#             doctor = request.user.doctorprofile
#             available_status = 'offline'
#             dav = DoctorAvailability.objects.filter(doctor=request.user.doctorprofile).update(available_days=available_days, available_start_time=available_start_time, available_end_time=available_end_time, available_status=available_status, doctor=doctor)
#             # dav_update = dav.update(available_days=available_days, available_start_time=available_start_time, available_end_time=available_end_time, available_status=available_status, doctor=doctor)
#             return HttpResponseRedirect(reverse('accounts:dashboard'))
#             # if da.update_or_create():
#             #     return HttpResponseRedirect(reverse('accounts:dashboard'))
#             # else:
#             #     return render(request, 'accounts/change_availability.html', {'form': form})            
#     else:
#         # doctorprofile = DoctorProfile.objects.get(doctor=request.user)
#         # dav = doctorprofile.doctoravailability
#         # av_days = dav.available_days
#         # av_start_time = dav.available_start_time
#         # av_end_time = dav.available_end_time
#         # av_status = dav.available_status
#         # data = {
#         #     'available_days': av_days,
#         #     'available_start_time': av_start_time,
#         #     'available_end_time': av_end_time,
#         #     'available_status': av_status,
#         #     'doctor': request.user
#         # }
#         # working_shifts = DoctorAvailability.objects.filter(doctor=request.user.doctorprofile).values('working_shifts')        
#         form = DoctorAvailabilityForm()
#     return render(request, 'accounts/change_availability.html', {'form': form})


def edit_working_shifts(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'doctor':
            if request.method == 'POST':
                form = DoctorWorkingShiftForm(request.POST)

                if form.is_valid():
                    doctor_profile = request.user.doctorprofile
                    working_day = form.cleaned_data['working_day']
                    start_time = form.cleaned_data['start_time']
                    end_time = form.cleaned_data['end_time']
                    obj, created = WorkingShift.objects.update_or_create(doctor_profile=doctor_profile, working_day=working_day, defaults = {'start_time':start_time, 'end_time': end_time})
                    # obj = form.save(commit=False)
                    # obj.doctor_profile = doctor_profile
                    # obj.save()
                    if obj:
                        return HttpResponseRedirect(reverse('accounts:edit_working_shifts'))

            else:
                form = DoctorWorkingShiftForm()
                working_shifts = WorkingShift.objects.filter(doctor_profile = request.user.doctorprofile)
                context = {
                    'form': form,
                    'working_shifts': working_shifts,
                }
            return render(request, 'accounts/change_availability.html', context)
        else:
            return HttpResponseRedirect(reverse('accounts:dashboard'))
            
