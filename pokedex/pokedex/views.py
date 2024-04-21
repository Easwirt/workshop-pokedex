from django.shortcuts import render

def home(request):
    links = {
        'links': [
        { 'title': 'Home', 'url': '/'},
        { 'title': 'Sign in', 'url': '/auth/signin'},
        { 'title': 'Sign Up', 'url': '/auth/signup'},
        ]
    }

    if request.user.is_authenticated:
        links['links'].pop()
        links['links'].pop()
        links['links'].append({ 'title': 'Pokémons', 'url': '/pokemons'})
        links['links'].append({ 'title': 'Logout', 'url': '/auth/signout'})
        links['links'].append({ 'title': 'Profile', 'url': '/id/'})

    return render(request, "home/home.tpl.html", context=links)
