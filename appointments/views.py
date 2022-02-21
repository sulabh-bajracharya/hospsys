from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateAppointmentForm, DoctorAvailabilityForm
from .models import Appointment
from accounts.models import User, DoctorProfile, WorkingShift
from django.contrib import messages
from django.views import generic

# Create your views here.
def index(request):
    return HttpResponse("Appointment page")

def choose_doctor(request):
    return render(request, 'appointments/choose_doctor.html')

def create(request):
    if request.method == 'POST':
        if 'availability_submit' in request.POST:
            availability_form = DoctorAvailabilityForm(request.POST)
            create_form = CreateAppointmentForm()
            
            if availability_form.is_valid():
                doctor = availability_form.cleaned_data['doctor']
                doctor_query = User.objects.get(email=doctor.email)
                shifts = WorkingShift.objects.filter(doctor_profile=doctor_query.doctorprofile)

                context = {
                    'create_form': create_form,
                    'availability_form': availability_form,
                    'working_shifts': shifts,
                    'doctor': doctor,
                }
                return render(request, 'appointments/create_appointment.html', context)

    #     form = CreateAppointmentForm(request.POST)
    #     if form.is_valid():
    #         doctor = form.cleaned_data['doctor']
    #         patient = request.user
    #         appointment_date = form.cleaned_data['appointment_date']
    #         appointment_time = form.cleaned_data['appointment_time']
    #         reason = form.cleaned_data['reason']
    #         description = form.cleaned_data['description']

    #         try:
    #             existing_appointment = Appointment.objects.get(doctor=doctor, patient=patient)
    #         except Appointment.DoesNotExist:
    #             existing_appointment = None

    #         if existing_appointment is not None:
    #             # messages.add_message(request, messages.ERROR, 'Appointment with doctor already exists.')
    #             messages.error(request,'Appointment with doctor already exists.')

    #             return HttpResponseRedirect(reverse('appointments:create_appointment'))
    #         else:
    #             obj, created = Appointment.objects.update_or_create(patient = patient, doctor=doctor,defaults={'doctor':doctor, 'appointment_date':appointment_date, 'appointment_time': appointment_time, 'reason':reason, 'description':description})
    #             if created:
    #                 return HttpResponseRedirect(reverse('accounts:dashboard'))
    #     else:
    #         messages.add_message(request, messages.ERROR, 'Invalid data')
    #         return render(request, 'accounts/patient_dashboard.html')
    else:
        create_form = CreateAppointmentForm()
        availability_form = DoctorAvailabilityForm()

        context = {
            'create_form': create_form,
            'availability_form': availability_form,
        }
    return render(request, 'appointments/create_appointment.html', context)

def doctor_availability(request):
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            doctor_query = User.objects.get(email=doctor.email)
            shifts = WorkingShift.objects.filter(doctor_profile=doctor_query.doctorprofile)
            return render(request, 'appointments/check_doctor_availability.html', {'form': form, 'working_shifts': shifts, 'doctor': doctor})
    else:
        form = DoctorAvailabilityForm()
    return render(request, 'appointments/check_doctor_availability.html', {'form': form})

def set_approval_status(request, pk):
    if request.method == 'POST':
        status = request.POST['approval_status']
        if status == 'Approve':
            approval_status = 'approved'
        if status == 'Reject':
            approval_status = 'rejected'
        if status == 'Pending':
            approval_status = 'pending'
        if status == 'Delete':
            approval_status = 'Deleted'
    try:
        appointment = Appointment.objects.get(pk=pk)
        appointment.approval_status = approval_status
        appointment.save()
        return HttpResponseRedirect(reverse('accounts:dashboard'))
    except Appointment.DoesNotExist:
        return HttpResponseRedirect(reverse('accounts:dashboard'))

def delete(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment Deleted.")
    return HttpResponseRedirect(reverse('accounts:dashboard'))

    
class AppointmentDetailView(generic.DetailView):
    model = Appointment
    template_name = 'appointments/appointment_details.html'
