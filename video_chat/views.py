from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context = {'name':"Sulabh"}
    return render(request, 'video_chat/main.html', context)

def chat(request, room_name):
    context = {'room_name': room_name}
    return render(request, 'video_chat/chat.html', context)

@login_required
def video(request):
    context = {}
    return render(request, 'video_chat/video.html', context)