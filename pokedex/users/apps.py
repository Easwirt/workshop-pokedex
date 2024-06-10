import warnings
from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

def warning_ignore(func):
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            return func(*args, **kwargs)
    return wrapper

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    @warning_ignore
    def ready(self):
        from .models import User
        post_save.connect(online_status_reset, sender=User)
        User = get_user_model()
        User.objects.all().update(online_status=0)

def online_status_reset(sender, instance, **kwargs):
    if instance.online_status != 0:
        instance.online_status = 0
        instance.save()