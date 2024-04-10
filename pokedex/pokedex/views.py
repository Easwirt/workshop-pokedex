from django.shortcuts import render

def home(request):
    links = {
        'links': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Pokémons', 'url': '/pokedex'},
            {'title': 'Admin', 'url': '/admin', 'target': '_new'},
            {'title': 'Sign Up', 'url': '/auth/signup', 'target': '_new'},
        ]
    }

    return render(request, "home.tpl.html", context=links)
