from django.shortcuts import render, get_object_or_404
from .models import Pokemon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def pokemonslist(request):
    pokemons_list = Pokemon.objects.all()
    paginator = Paginator(pokemons_list, 20)

    page = request.GET.get('page')
    try:
        pokemons = paginator.page(page)
    except PageNotAnInteger:
        pokemons = paginator.page(1)
    except EmptyPage:
        pokemons = paginator.page(paginator.num_pages)

    return render(request, 'pokemons/pokemons-list.tpl.html', {'pokemons': pokemons})



def pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    return render(request, 'pokemons/pokemon-detail.tpl.html', {'pokemon': pokemon})