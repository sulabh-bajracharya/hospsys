from django.contrib import admin
from django.urls import path, include
from . import views
from .views import AppointmentDetailView

app_name = 'appointments'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/<int:doctor_id>', views.create, name='create_appointment'),
    path('edit/<int:appointment_id>', views.edit, name='edit_appointment'),
    path('doctors/', views.doctors, name='list_doctors'),
    path('doctor-availability/', views.doctor_availability, name='doctor_availability'),
    path('approve-status/<int:pk>', views.set_approval_status, name='set_approval_status'),
    path('details/<int:pk>', AppointmentDetailView.as_view(), name='view_details'),
    path('delete/<int:appointment_id>', views.delete, name='delete_appointment'),
    path('cancel/<int:appointment_id>', views.cancel_appointment, name='cancel_appointment'),
]

