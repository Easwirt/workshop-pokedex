from django.contrib import admin
from .models import User, EmailVerificationToken

admin.site.register(EmailVerificationToken)
admin.site.register(User)