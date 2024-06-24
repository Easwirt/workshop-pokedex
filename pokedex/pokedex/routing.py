from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('ws/online/', consumers.PokemonConsumer.as_asgi()),
    re_path(r'ws/fight/(?P<fight_id>\w+)/$', consumers.FightConsumer.as_asgi()),
]
