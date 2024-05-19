from django.contrib import admin
from .models import User, EmailVerificationToken, Profile, RecentActivity, Achievement, UserAchievement

admin.site.register(EmailVerificationToken)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(RecentActivity)
admin.site.register(Achievement)
admin.site.register(UserAchievement)