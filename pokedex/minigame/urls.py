from django.urls import path
from .views import minigame

urlpatterns = [
    path('', minigame, name='minigame')
]