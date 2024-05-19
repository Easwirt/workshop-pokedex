from django.db import models
from django.contrib.auth.models import AbstractUser
from pokemons.models import Pokemon
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pokemons = models.ManyToManyField(Pokemon, blank=True)
    bio = models.TextField(max_length=300)
    avatar = models.IntegerField(default=0)
    coins = models.IntegerField(default=100)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Profile.objects.create(user=instance)
        achievement, _ = Achievement.objects.get_or_create(
            name="New Catcher",
            defaults={'description': 'New user achievement', 'icon': 0}
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


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.IntegerField()
    users = models.ManyToManyField(User, through='UserAchievement')

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.achievement.name} - {self.date_awarded}'