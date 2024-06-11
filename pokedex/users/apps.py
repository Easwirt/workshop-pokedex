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