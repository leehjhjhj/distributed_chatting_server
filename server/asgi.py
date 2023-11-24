
import os
from channels.routing import URLRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from socket_app.routings import chat_routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.local.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(
        chat_routing.websocket_urlpatterns
    )
})