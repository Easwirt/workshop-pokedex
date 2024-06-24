import json
from django.conf import settings
from users.views import send_mail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.response import TemplateResponse
from .models import User, RecentActivity, Profile
from .helpers import give_daily_reward
from achievements.models import UserAchievement
from django.shortcuts import get_object_or_404, redirect, render
from pokemons.helpers import paginacia
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import authenticate, login

@login_required(login_url='/auth/signin/')
def profile_view(request, username=None):
    query = request.GET.get('query')
    
    if query:
        users = User.objects.filter(username__icontains=query, is_staff=False)
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

    privacy = profile.privacy
    is_friend = request.user in profile.friends.all()

    data = {
        'defaultURL': settings.DEFAULT_URL,
        'friendsRequest': user.profile.friends_request.exclude(id=user.id),
        'requestUserName': request.user.username,
        'friends': friends,
        'id': user.id,
        'profile': profile,
        'is_friend': is_friend,
        'privacy': privacy,
        'user_pokemons_paginacia': user_pokemons_paginacia,
        'change_permission': change_permission,
        'achievements': achievements,
        'activities': activities,
        'online_status': online_status,
    }

    return TemplateResponse(request, 'profile/profile.tpl.html', data)


@login_required(login_url='/auth/signin/')
def daily_reward(request):
    profile = Profile.objects.get(user=request.user)
    success, bonus_coins, remaining_hours, remaining_minutes = give_daily_reward(profile)
    if success:
        messages.success(request, f'Bonus received! You have been awarded 100 🪙 plus {bonus_coins} bonus 🪙 for your pokemons.')
    else:
        messages.error(request, f'You can receive the next bonus after {int(remaining_hours)} hours and {int(remaining_minutes)} minutes.')
    return redirect('my-profile')


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
def accept_friend_request(request, friendname):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    friend = get_object_or_404(User, username=friendname)

    user.profile.friends.add(friend)
    friend.profile.friends.add(user)

    user.profile.friends_request.remove(friend)
    friend.profile.friends_request.remove(user)
    RecentActivity.objects.create(user=request.user, activity_type=f'{user.username} now friend with {friend.usernamename}')
    return JsonResponse({'status': 'success', 'message': 'Friend request accepted.'})

@login_required(login_url='/auth/signin/')
def remove_user_from_friend(request, username, friendname):
    user = get_object_or_404(User, username=username)
    friend = get_object_or_404(User, username=friendname)
    user.profile.friends.remove(friend)
    friend.profile.friends.remove(user)

    return JsonResponse({'status': 'success', 'message': 'User removed.'})

@login_required(login_url='auth/signin/')
def show_friends(request):
    friends = request.user.profile.friends_request.all()
    data = []
    for friend in friends:
        friend = friend
        data.append({
            'username': friend.username,
            'avatar': friend.profile.avatar,
        })

    return JsonResponse({'friends': data})

@login_required(login_url='/auth/signin/')
def decline_friend_request(request, friendname):
    user = get_object_or_404(User, username=request.user.username)
    friend = get_object_or_404(User, username=friendname)
    user.profile.friends_request.remove(friend)
    return JsonResponse({'status': 'success', 'message': 'Friend request declined.'})


# EDIT PROFILE SECTION
# EDIT PROFILE SECTION
# EDIT PROFILE SECTION

@login_required(login_url='/auth/signin/')
def edit_profile(request):

    user = request.user
    profile = user.profile

    user_pokemons = user.profile.pokemons.all()
    page_number = request.GET.get('page')
    user_pokemons_paginacia = paginacia(user_pokemons, page_number, per_page=12) 

    achievements = UserAchievement.objects.filter(user=user)[:8]
    activities = RecentActivity.objects.filter(user=user).order_by('-timestamp')[:10]
    online_status = profile.user.online_status

    friends = profile.friends.all()

    data = {
        'defaultURL': settings.DEFAULT_URL,
        'friendsRequest': user.profile.friends_request.exclude(id=user.id),
        'requestUserName': request.user.username,
        'friends': friends,
        'id': user.id,
        'profile': profile,
        'user_pokemons_paginacia': user_pokemons_paginacia,
        'achievements': achievements,
        'activities': activities,
        'online_status': online_status,
    }

    return TemplateResponse(request, 'profile/editprofile.tpl.html', data)



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




@login_required(login_url='/auth/signin/')
def clear_recent_activity(request):
    if request.method == 'POST':
        user = request.user
        RecentActivity.objects.filter(user=user).delete()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    


@login_required(login_url='/auth/signin/')
def update_bio(request, new_bio):
    if request.method == 'POST':

        request.user.profile.bio = new_bio
        request.user.profile.save()

        return JsonResponse({'success': True})
    else:
        return redirect('edit-profile')
    
@login_required(login_url='/auth/signin/')
def change_password(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8')) 
        old_password = data.get('old_password')
        new_password1 = data.get('new_password1')

        user = authenticate(username=request.user.username, password=old_password)
        if user is None:
            return JsonResponse({'success': False, 'error': 'Incorrect old password.'}, status=400)

        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'User is not authenticated.'}, status=401)

        login(request, user)

        subject = 'Password changed'
        message = 'Your password has been changed successfully.'
        send_mail(user=user, subject=subject, message=message)
        user.set_password(new_password1)
        user.save()

        return JsonResponse({'success': True, 'message': 'Password changed successfully.'})
    else:
        return redirect('edit-profile')


@login_required(login_url='/auth/signin/')
def update_privacy(request):
    if request.method == 'POST':
        privacy_value = request.POST.get('privacy_value')

        if privacy_value in ['0', '1', '2']:
            profile = Profile.objects.get(user=request.user)
            profile.privacy = int(privacy_value)
            profile.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid privacy value'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed.'}, status=405)