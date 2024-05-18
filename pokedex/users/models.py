from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from pokemons.models import Pokemon

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


class RecentActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.activity_type} - {self.timestamp}'


@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def saveprofile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.profile.save()
