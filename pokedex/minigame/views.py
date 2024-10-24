from django.shortcuts import render
from .models import Boss, Fight
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/signin/')
def minigame(request):
    user = request.user
    profile = user.profile

    boss_number = profile.boss
    boss = Boss.objects.filter(id=boss_number).first()

    if boss is None:
        return render(request, "minigame/minigame.end.tpl.html")
    
    fight = Fight.objects.filter(profile=profile).first()

    if not fight:
        fight = Fight.objects.create(boss=boss, profile=profile)
    elif fight.status != 1:
        fight.delete()
        fight = Fight.objects.create(boss=boss, profile=profile)


    return render(request, "minigame/minigame.tpl.html", {'boss': boss, 'fight': fight})
