"""
ASGI config for hospsys project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import video_chat.routing
import appointments.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospsys.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            video_chat.routing.websocket_urlpatterns,
            # appointments.routing.websocket_urlpatterns,
        )
    )
})
