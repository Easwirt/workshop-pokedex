import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User, Trade
from pokemons.models import Pokemon
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

def save_trade(request):
    if request.method == 'POST':
        try:
            # Assuming the POST data is JSON
            data = json.loads(request.body)
            friend = get_object_or_404(User, username=data['receiver'])

            # Create the Trade instance without ManyToMany fields
            trade = Trade.objects.create(sender=request.user, receiver=friend)

            # Add pokemons_send to the ManyToMany field
            pokemons_send = Pokemon.objects.filter(id__in=data['pokemons_send'])
            trade.pokemons_send.set(pokemons_send)

            # Add pokemons_received to the ManyToMany field
            pokemons_received = Pokemon.objects.filter(id__in=data['pokemons_received'])
            trade.pokemons_received.set(pokemons_received)

            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Pokemon.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid Pokemon ID'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def show_trade(request):
    trades = Trade.objects.filter(receiver=request.user)
    ret = []
    for trade in trades:
        trade_info = {
            'sender': trade.sender.username,
            'receiver': trade.receiver.username,
            'pokemons_send': {
                'name': [pokemon.name for pokemon in trade.pokemons_send.all()],
                'id': [pokemon.id for pokemon in trade.pokemons_send.all()],
            },
            'pokemons_received': {
                'name': [pokemon.name for pokemon in trade.pokemons_received.all()],
                'id': [pokemon.id for pokemon in trade.pokemons_received.all()],
            },
            'sender_avatar': trade.sender.profile.avatar,
        }
        ret.append(trade_info)
    return JsonResponse({'trades': ret})

def accept_trade(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            friend = get_object_or_404(User, username=data['friend'])
            trades = Trade.objects.filter(sender=friend, receiver=request.user)
            trade = trades[data['id']]
            for pokemon in trade.pokemons_send.all():
                request.user.profile.pokemons.add(pokemon)

            for pokemon in trade.pokemons_received.all():
                friend.profile.pokemons.add(pokemon)

            return JsonResponse({'success': trade.sender.profile.user.username})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Pokemon.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid Pokemon ID'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
