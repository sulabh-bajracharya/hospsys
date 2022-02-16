from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'', consumers.VideoConsumer.as_asgi()),
    # re_path('ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path('(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()),
    # re_path('video_chat/room/(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()),
    # re_path('video_chat/(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()),
    re_path('appointments/create/', consumers.GetDoctorShiftConsumer.as_asgi()),


]