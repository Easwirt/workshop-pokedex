from django.urls import path, include
from .views import pokemonslist, pokemon

urlpatterns = [
    path('', pokemonslist, name='pokemons'),
    path('<int:pokemon_id>/', pokemon, name='pokemon'),
]
