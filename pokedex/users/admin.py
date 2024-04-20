from django.contrib import admin
from .models import User, EmailVerificationToken, Profile

admin.site.register(EmailVerificationToken)
admin.site.register(User)
admin.site.register(Profile)