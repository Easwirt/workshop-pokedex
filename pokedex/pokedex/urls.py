from django.contrib import admin
from django.urls import path, include
from .views import home
from users.views import profile_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home-page"),
    path('auth/', include('users.urls')),
    path('profile/', profile_view, name='my-profile'),
    path('profile/<str:username>/', profile_view, name='user-profile'),
    path('pokemons/', include('pokemons.urls')),
]
