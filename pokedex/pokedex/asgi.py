import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokedex.settings')

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import routing
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async



User = get_user_model()

@sync_to_async
def update_user_status():
    User.objects.all().update(online_status=0)

class Protocol(ProtocolTypeRouter):
    async def __call__(self, scope, receive, send):
        await update_user_status()
        return await super().__call__(scope, receive, send)


django_asgi_app = get_asgi_application()

application = Protocol({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
