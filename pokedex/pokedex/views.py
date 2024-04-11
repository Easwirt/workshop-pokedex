from django.shortcuts import render

def home(request):
    links = {
        'links': [
        { 'title': 'Home', 'url': '/'},
        { 'title': 'Pokémons', 'url': '/pokedex'},
        { 'title': 'Sign in', 'url': '/auth/signin'},
        { 'title': 'Sign Up', 'url': '/auth/signup'},
        ]
    }

    if request.user.is_authenticated:
        links['links'].pop()
        links['links'].append({ 'title': 'Logout', 'url': '/auth/signout'})

    return render(request, "home.tpl.html", context=links)
