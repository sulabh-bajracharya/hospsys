from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'video_chat'
urlpatterns = [
    path('', views.video, name='video'),
    path('<str:room_name>/', views.chat, name='chat'),
    path('room/<str:room_name>/', views.video, name='video_room'),
]