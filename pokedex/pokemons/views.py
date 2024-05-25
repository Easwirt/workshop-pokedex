from django.shortcuts import render, get_object_or_404
from .models import Pokemon
from profiles.models import Profile, RecentActivity
from .forms import SearchForm, PurchasePokemonForm, SellPokemonForm
from django.contrib.auth.decorators import login_required
from .helpers import paginacia, levinstain
from django.shortcuts import redirect
from django.contrib import messages

@login_required(login_url='/auth/signin/')
def pokemonslist(request):
    form = SearchForm(request.GET)
    message = None
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            if query.isdigit():
                pokemon = get_object_or_404(Pokemon, id=query)
                return render(request, 'pokemons/pokemon-detail.tpl.html', {'pokemon': pokemon})
            else:
                pokemons_list = Pokemon.objects.filter(name__icontains=query)
                pokemons = paginacia(pokemons_list, request.GET.get('page'))
                if not pokemons:
                    closest_pokemon = levinstain(query)
                    message = f'Pokémon "{query}" sa nenašiel :-('
                    message += f"<br>Maybe you mean <a href='/pokemons/{closest_pokemon.id}/'>{closest_pokemon.name}</a>?"
    else:
        pokemons_list = Pokemon.objects.all()
        pokemons = paginacia(pokemons_list, request.GET.get('page'))

    return render(request, 'pokemons/pokemons-list.tpl.html', {'pokemons': pokemons, 'error_message': message})



@login_required(login_url='/auth/signin/')
def pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    return render(request, 'pokemons/pokemon-detail.tpl.html', {'pokemon': pokemon})

@login_required(login_url='/auth/signin/')
def purchasepokemon(request):
    if request.method == 'POST':
        form = PurchasePokemonForm(request.POST)
        if form.is_valid():
            pokemon_id = form.cleaned_data['pokemon_id']
            pokemon = get_object_or_404(Pokemon, id=pokemon_id)
            profile = get_object_or_404(Profile, user=request.user)


            if profile.pokemons.filter(id=pokemon_id).exists():
                error_message = f'You already bought pokemon {pokemon.name}.'
                messages.error(request, error_message)
                return redirect('/profile')

            if profile.coins >= pokemon.price:
                profile.coins -= pokemon.price
                profile.pokemons.add(pokemon)
                profile.save()
                RecentActivity.objects.create(user=request.user, activity_type=f'Purchase Pokemon - {pokemon.name}, {pokemon.price}$')
                success_message = f'You bought {pokemon.name}!'
                messages.error(request, success_message)
                return redirect('/profile')
            else:
                error_message = f'You dont have enough money to buy this pokemon. You have {profile.coins}'
                messages.error(request, error_message)
                return redirect('/profile')

    return redirect('/profile')


@login_required(login_url='/auth/signin/')
def sellpokemon(request):
    if request.method == 'POST':
        form = SellPokemonForm(request.POST)
        if form.is_valid():
            pokemon_id = form.cleaned_data['pokemon_id']
            profile = get_object_or_404(Profile, user=request.user)
            pokemon = get_object_or_404(Pokemon, id=pokemon_id)

            if profile.pokemons.filter(id=pokemon_id).exists():
                profile.pokemons.remove(pokemon)
                profile.coins += pokemon.price // 2
                profile.save()
                RecentActivity.objects.create(user=request.user, activity_type=f'Sold Pokemon - {pokemon.name}')
                success_message = f'You sold {pokemon.name} for {pokemon.price // 2}$!'
                messages.success(request, success_message)
            else:
                error_message = f'You dont have {pokemon.name}.'
                messages.error(request, error_message)
        
            return redirect('/profile')

    return redirect('/profile')