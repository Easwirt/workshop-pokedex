from django.contrib import admin
from django.urls import path, include
from .views import home
from users.views import profile_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home-page"),
    path('auth/', include('users.urls')),
    path('id/', profile_view, name='profile'),
    path('pokemons/', include('pokemons.urls')),
]
