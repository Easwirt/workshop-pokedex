from django.shortcuts import render, get_object_or_404
from .models import Pokemon
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from .helpers import paginacia, levinstain

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

