from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, DoctorWorkingShiftForm
from django.urls import reverse
from .models import DoctorAvailability, DoctorProfile, WorkingShift, User
from django.views.generic.edit import UpdateView
from appointments.models import Appointment
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

# Create your views here.
def index(request):
    return HttpResponse("index page.")

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request,'Please verify your account before logging in.')
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        messages.success(request,'Account verified. You can login now.')
        return HttpResponseRedirect(reverse('accounts:login'))
    else:
        return HttpResponse('Activation link is invalid!')

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
            
