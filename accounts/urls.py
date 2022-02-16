from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('working_shifts/edit/', views.edit_working_shifts, name='edit_working_shifts'),
    path('working_shifts/', views.view_working_shifts, name='view_working_shifts'),
    # path('', views.index),
]
