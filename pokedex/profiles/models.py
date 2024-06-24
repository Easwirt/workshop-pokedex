from django.db import models
from pokemons.models import Pokemon
from django.db.models.signals import post_save
from django.dispatch import receiver
from achievements.models import Achievement, UserAchievement
from users.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pokemons = models.ManyToManyField(Pokemon, blank=True)
    bio = models.TextField(max_length=100, default="Hi, there!")
    avatar = models.IntegerField(default=0)
    coins = models.IntegerField(default=100)
    last_bonus_time = models.DateTimeField(null=True, blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    friends_request = models.ManyToManyField(User, related_name='friends_request', blank=True)
    privacy = models.IntegerField(default=0)
    boss = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Profile.objects.create(user=instance)
        achievement, _ = Achievement.objects.get_or_create(
            name="New Catcher",
            defaults={'description': 'Welcome!', 'icon': 0}
        )
        UserAchievement.objects.create(user=instance, achievement=achievement)
        
@receiver(post_save, sender=User)
def saveprofile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.profile.save()
    
class RecentActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.activity_type} - {self.timestamp}'