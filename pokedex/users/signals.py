from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Pokemon, Achievement, UserAchievement, RecentActivity
from django.contrib.auth.models import User
from .models import Profile


@receiver(m2m_changed, sender=Profile.pokemons.through)
def update_achievements(sender, instance, **kwargs):
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    
    if action == 'post_add':
        user = instance.user
        num_pokemons = user.profile.pokemons.count()
        
        achievements = [
            (5, "Catcher", "Got 5 pokemons", 1),
            (10, "Gold Catcher", "Got 10 pokemons", 2),
            (15, "Diamond Catcher", "Got 15 pokemons", 3),
            (30, "Brilliant Catcher", "Got 30 pokemons", 4),
        ]
        
        current_achievements = set(user.userachievement_set.values_list('achievement__name', flat=True))
        
        for threshold, name, description, icon_number in achievements:
            if num_pokemons >= threshold and name not in current_achievements:
                achievement, created = Achievement.objects.get_or_create(
                    name=name,
                    defaults={'description': description, 'icon': icon_number}
                )
                UserAchievement.objects.create(user=user, achievement=achievement)
                RecentActivity.objects.create(user=user, activity_type=f"Reach achievement {name}")
