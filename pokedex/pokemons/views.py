from django.shortcuts import render, get_object_or_404
from .models import Pokemon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from django.contrib.auth.decorators import login_required


def paginacia(objects, page_number, per_page=20):
    paginator = Paginator(objects, per_page)

    try:
        paginated_objects = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects

@login_required(login_url='/auth/signin/')
def pokemonslist(request):
    form = SearchForm(request.GET)
    message = "Pokémon sa nenašiel :-("
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            if query.isdigit():
                pokemon = get_object_or_404(Pokemon, id=query)
                return render(request, 'pokemons/pokemon-detail.tpl.html', {'pokemon': pokemon})
            else:
                pokemons_list = Pokemon.objects.filter(name__icontains=query)
                pokemons = paginacia(pokemons_list, request.GET.get('page'))
        
    else:
        pokemons_list = Pokemon.objects.all()
        pokemons = paginacia(pokemons_list, request.GET.get('page'))

    return render(request, 'pokemons/pokemons-list.tpl.html', {'pokemons': pokemons, 'error_message' : message})

@login_required(login_url='/auth/signin/')
def pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    return render(request, 'pokemons/pokemon-detail.tpl.html', {'pokemon': pokemon})

