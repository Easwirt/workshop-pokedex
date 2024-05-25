from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)