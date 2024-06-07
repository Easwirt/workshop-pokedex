from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from .models import User, RecentActivity
from achievements.models import UserAchievement
from django.shortcuts import get_object_or_404, redirect, render
from pokemons.helpers import paginacia

@login_required(login_url='/auth/signin/')
def profile_view(request, username=None):
    query = request.GET.get('query')
    
    if query:
        users = User.objects.filter(username__icontains=query)
        return render(request, 'auth/profilessearch.tpl.html', {'users': users, 'query': query})
    elif query is '':
        users = User.objects.filter(is_staff=False)[:8]
        return render(request, 'auth/profilessearch.tpl.html', {'users': users})

    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    change_permission = user.username == request.user.username
    
    profile = user.profile

    user_pokemons = user.profile.pokemons.all()
    page_number = request.GET.get('page')
    user_pokemons_paginacia = paginacia(user_pokemons, page_number, per_page=12) 

    achievements = UserAchievement.objects.filter(user=user)[:4]
    activities = RecentActivity.objects.all().order_by('-timestamp')[:10]
    online_status = profile.user.online_status

    data = {
        'id': user.id,
        'profile': profile,
        'user_pokemons_paginacia': user_pokemons_paginacia,
        'change_permission': change_permission,
        'achievements': achievements,
        'activities': activities,
        'online_status': online_status,
    }

    return TemplateResponse(request, 'auth/profile.tpl.html', data)


@login_required(login_url='/auth/signin/')
def change_avatar(request, avatar):
    avatar = int(avatar)
    if avatar < 0 or avatar > 10:
        return redirect('/profile/')


    user = request.user
    profile = user.profile
    profile.avatar = avatar
    profile.save()

    return redirect('/profile/')


@login_required(login_url='/auth/signin/')
def edit_profile(request):
    pass