from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.response import TemplateResponse
from .models import User, RecentActivity, Profile
from .helpers import give_daily_reward
from .forms import BioForm
from achievements.models import UserAchievement
from django.shortcuts import get_object_or_404, redirect, render
from pokemons.helpers import paginacia
from django.contrib import messages
from django.db.models import Count

@login_required(login_url='/auth/signin/')
def profile_view(request, username=None):
    query = request.GET.get('query')
    
    if query:
        users = User.objects.filter(username__icontains=query)
        return render(request, 'auth/profilessearch.tpl.html', {'users': users, 'query': query})
    elif query == '':
        users = User.objects.filter(is_staff=False).annotate(num_pokemons=Count('profile__pokemons')).order_by('-num_pokemons')[:8]
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

    achievements = UserAchievement.objects.filter(user=user)[:8]
    activities = RecentActivity.objects.filter(user=user).order_by('-timestamp')[:10]
    online_status = profile.user.online_status

    friends = profile.friends.all()

    print(user.profile.friends_request.all())
    data = {
        'defaultURL': settings.DEFAULT_URL,
        'friendsRequest': user.profile.friends_request.exclude(id=user.id),
        'requestUserName': request.user.username,
        'friends': friends,
        'id': user.id,
        'profile': profile,
        'user_pokemons_paginacia': user_pokemons_paginacia,
        'change_permission': change_permission,
        'achievements': achievements,
        'activities': activities,
        'online_status': online_status,
    }

    return TemplateResponse(request, 'profile/profile.tpl.html', data)


@login_required(login_url='/auth/signin/')
def change_avatar(request, avatar):
    avatar = int(avatar)
    if avatar < 0 or avatar > 10:
        return redirect('/profile/')


    user = request.user
    profile = user.profile
    profile.avatar = avatar
    profile.save()
    messages.success(request, 'Avatar changed!')

    return redirect('/profile/editprofile/')


@login_required
def daily_reward(request):
    profile = Profile.objects.get(user=request.user)
    success, bonus_coins, remaining_hours, remaining_minutes = give_daily_reward(profile)
    if success:
        messages.success(request, f'Bonus received! You have been awarded 100 coins plus {bonus_coins} bonus coins for your pokemons.')
    else:
        messages.error(request, f'You can receive the next bonus after {int(remaining_hours)} hours and {int(remaining_minutes)} minutes.')
    return redirect('my-profile')


@login_required(login_url='/auth/signin/')
def edit_profile(request):
    if request.method == 'POST':
        form = BioForm(request.POST)
        if form.is_valid():
            new_bio = form.cleaned_data['bio']
            request.user.profile.bio = new_bio
            request.user.profile.save()
            messages.success(request, 'Bio updated!')
            return TemplateResponse(request, 'profile/editprofile.tpl.html', {'form': form})
        else:
            message = "Invalid bio"
            form.add_error('bio', message)
            return TemplateResponse(request, 'profile/editprofile.tpl.html', {'form': form})
    else:
        form = BioForm()
    return TemplateResponse(request, 'profile/editprofile.tpl.html', {'form': form})


@login_required(login_url='/auth/signin/')
def friend_request(request, username, friendname):
    user = get_object_or_404(User, username=username)
    friend = get_object_or_404(User, username=friendname)
    if user in friend.profile.friends_request.all() or user in friend.profile.friends.all():
        return JsonResponse({'status': 'error', 'message': 'Friend request already sent.'})
    else:
        friend.profile.friends_request.add(user)
        return JsonResponse({'status': 'success', 'message': 'Friend request sent.'})

@login_required(login_url='/auth/signin/')
def accept_friend_request(request, username, friendname):
    user = get_object_or_404(User, username=username)
    friend = get_object_or_404(User, username=friendname)

    user.profile.friends.add(friend)
    friend.profile.friends.add(user)

    user.profile.friends_request.remove(friend)
    friend.profile.friends_request.remove(user)
    return JsonResponse({'status': 'success', 'message': 'Friend request accepted.'})

@login_required(login_url='/auth/signin/')
def remove_user_from_friend(request, username, friendname):
    user = get_object_or_404(User, username=username)
    friend = get_object_or_404(User, username=friendname)
    user.profile.friends.remove(friend)
    friend.profile.friends.remove(user)

    return JsonResponse({'status': 'success', 'message': 'User removed.'})
