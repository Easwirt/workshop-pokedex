from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/online/', consumers.PokemonConsumer.as_asgi()),
]
