from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from .models import User, RecentActivity
from achievements.models import UserAchievement
from django.shortcuts import get_object_or_404, redirect

@login_required(login_url='/auth/signin/')
def profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    if user.username == request.user.username:
        change_permission = True
    else:
        change_permission = False
    
    profile = user.profile
    user_pokemons = request.user.profile.pokemons.all()
    achievements = UserAchievement.objects.filter(user=user)[:4]
    activities = RecentActivity.objects.all().order_by('-timestamp')[:10]

    data = {
        'profile': profile,
        'user_pokemons': user_pokemons,
        'change_permission': change_permission,
        'achievements': achievements,
        'activities': activities,
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
    # change bio, change password (maybe something else)