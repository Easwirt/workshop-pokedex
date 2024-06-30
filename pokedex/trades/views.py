from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User


def trade_list(request, friendname):
    print('New trade', friendname)
    friend = get_object_or_404(User, username=friendname)
    user_pokemons = request.user.profile.pokemons.all()
    pokemon_list = [
        {
            'id': pokemon.id,
            'name': pokemon.name,
        }
        for pokemon in user_pokemons
    ]

    friend_pokemons = friend.profile.pokemons.all()
    friend_pokemon_list = [
        {
            'id': pokemon.id,
            'name': pokemon.name,
        }
        for pokemon in friend_pokemons
    ]

    return JsonResponse({'pokemons': pokemon_list,
                         'friendpokemons': friend_pokemon_list,
                         'user_money': request.user.profile.coins,
                         'friend_money': friend.profile.coins})

