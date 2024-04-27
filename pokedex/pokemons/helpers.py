from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Levenshtein import distance as lev
from .models import Pokemon

def paginacia(objects, page_number, per_page=20):
    paginator = Paginator(objects, per_page)

    try:
        paginated_objects = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects



def levinstain(word):
    pokemons_list = Pokemon.objects.all()
    min = float('inf')
    
    for pokemon in pokemons_list:
        distance = lev(word.lower(), pokemon.name.lower())
        if distance < min:
            min = distance
            closest_pokemon = pokemon

    return closest_pokemon