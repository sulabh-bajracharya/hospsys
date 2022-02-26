from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse

app_name = 'accounts'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('register_profile/<str:user_type>/', views.register_profile, name='register_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='/accounts/login/'), name='password_change'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password/password_reset.html'), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password/password_reset_complete.html'), name='password_reset_complete'), 
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('', views.dashboard, name='dashboard'),
    path('working_shifts/edit/', views.edit_working_shifts, name='edit_working_shifts'),
    path('working_shifts/', views.view_working_shifts, name='view_working_shifts'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    # path('', views.index),
]
