from django.urls import path, include
from .views import pokemonslist, pokemon, purchasepokemon

urlpatterns = [
    path('', pokemonslist, name='pokemons'),
    path('<int:pokemon_id>/', pokemon, name='pokemon'),
    path('purchase-pokemon/', purchasepokemon, name='purchase-pokemon'),
]
