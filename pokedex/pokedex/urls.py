from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home-page"),
    path('auth/', include('users.urls')),
    path('profile/', include('profiles.urls')),
    path('pokemons/', include('pokemons.urls')),
    path('game/', include('minigame.urls')),
]
