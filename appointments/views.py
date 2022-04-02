from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateAppointmentForm, DoctorAvailabilityForm, EditAppointmentForm
from .models import Appointment
from accounts.models import User, DoctorProfile, WorkingShift, Department
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return HttpResponse("Appointment page")

@login_required
def choose_doctor(request):
    return render(request, 'appointments/choose_doctor.html')

@login_required
def create(request, doctor_id):
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
        if 'create_appointment_submit' in request.POST:
            form = CreateAppointmentForm(request.POST, request.FILES)

            if form.is_valid():
                doctor = User.objects.get(pk=doctor_id)
                patient = request.user
                appointment_date = form.cleaned_data['appointment_date']
                appointment_time = form.cleaned_data['preferred_appointment_time']
                reason = form.cleaned_data['reason']
                description = form.cleaned_data['description']
                breakpoint()

                history_files = request.FILES['files'].name

                try:
                    existing_appointment = Appointment.objects.get(doctor=doctor, patient=patient)
                except Appointment.DoesNotExist:
                    existing_appointment = None

                if existing_appointment is not None:
                    # messages.add_message(request, messages.ERROR, 'Appointment with doctor already exists.')
                    messages.error(request,'You already have an appointment with this doctor. Please check your dashboard for your appointments.')

                    return HttpResponseRedirect(reverse('appointments:create_appointment', args=(doctor_id,)))
                else:
                    doctor_appointments = Appointment.objects.filter(doctor=doctor)
                    for appoint in doctor_appointments:
                        if int(appoint.appointment_time) == int(appointment_time):
                            messages.error(request, 'The time slot is already booked. Please try another time slot for appointment')
                            return HttpResponseRedirect(reverse('appointments:create_appointment', args=(doctor_id,)))
                            
                    obj, created = Appointment.objects.update_or_create(patient = patient, doctor=doctor,defaults={'doctor':doctor, 'appointment_date':appointment_date, 'appointment_time': appointment_time, 'reason':reason, 'description':description, 'history_files': history_files })
                    if created:
                        return HttpResponseRedirect(reverse('accounts:dashboard'))
            else:
                messages.add_message(request, messages.ERROR, 'Invalid data')
                return render(request, 'accounts/patient_dashboard.html')
    else:
        doctor = User.objects.get(pk=doctor_id)
        request.session['doctor_id'] = doctor_id
        working_shifts = WorkingShift.objects.filter(doctor_profile=doctor.doctorprofile)
        create_form = CreateAppointmentForm()
        availability_form = DoctorAvailabilityForm()

        context = {
            'create_form': create_form,
            'availability_form': availability_form,
            'doctor': doctor,
            'working_shifts': working_shifts,
        }
    return render(request, 'appointments/create_appointment.html', context)

@login_required
def edit(request, appointment_id):
    if request.method == 'POST':
        appointment = Appointment.objects.get(pk=appointment_id)
        doctor = appointment.doctor
        form = EditAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            doctor_appointments = Appointment.objects.filter(doctor=doctor)
            for appoint in doctor_appointments:
                if (appoint.patient != request.user and int(appoint.appointment_time) == int(appointment.appointment_time)):
                    messages.error(request, 'The time slot is already booked. Please try another time slot for appointment')
                    return HttpResponseRedirect(reverse('appointments:edit_appointment', args=(appointment.id,)))
            # appointment_date = form.cleaned_data['appointment_date']
            # appointment_time = form.cleaned_data['appointment_time']
            # reason = form.cleaned_data['reason']
            # description = form.cleaned_data['description']
            form.save()
            messages.success(request, "Appointment updated successfully.")
            return HttpResponseRedirect(reverse('appointments:view_details', args=(appointment.id,)))

    appointment = Appointment.objects.get(pk=appointment_id)
    form = EditAppointmentForm(instance=appointment)
    context = {
        'appointment': appointment,
        'edit_form': form,
    }
    return render(request, 'appointments/edit_appointment.html', context)

@login_required
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

@login_required
def set_approval_status(request, pk):
    if request.method == 'POST':
        status = request.POST['approval_status']
        if status == 'Approve':
            approval_status = 'approved'
        if status == 'Reject':
            approval_status = 'rejected'
        if status == 'Pending':
            approval_status = 'pending'
        if status == 'Cancel':
            approval_status = 'cancelled'
        if status == 'Delete':
            approval_status = 'deleted'
    try:
        appointment = Appointment.objects.get(pk=pk)
        appointment.approval_status = approval_status
        appointment.save()
        return HttpResponseRedirect(reverse('accounts:dashboard'))
    except Appointment.DoesNotExist:
        return HttpResponseRedirect(reverse('accounts:dashboard'))

@login_required
def delete(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment Deleted.")
    return HttpResponseRedirect(reverse('accounts:dashboard'))
 
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.approval_status = 'cancelled'
    appointment.save()
    return HttpResponseRedirect(reverse('accounts:dashboard'))

@login_required
def doctors(request):
    doctors = User.objects.filter(user_type='doctor')
    departments = Department.objects.all()
    context = {
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'appointments/doctors.html', context)


class AppointmentDetailView(generic.DetailView):
    model = Appointment
    template_name = 'appointments/appointment_details.html'
