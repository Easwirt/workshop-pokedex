from django.urls import path
from .views import pokemonslist, pokemon, purchasepokemon, sellpokemon

urlpatterns = [
    path('', pokemonslist, name='pokemons'),
    path('<int:pokemon_id>/', pokemon, name='pokemon'),
    path('purchase-pokemon/', purchasepokemon, name='purchase-pokemon'),
    path('sell-pokemon/', sellpokemon, name='sell-pokemon'),
]