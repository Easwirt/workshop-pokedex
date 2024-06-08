from django.urls import path
from .views import profile_view, change_avatar, edit_profile, daily_reward


urlpatterns = [
    path('dailyreward/', daily_reward, name='daily-reward'),
    path('changeavatar/<int:avatar>/', change_avatar, name='change-avatar'),
    path('<str:username>/', profile_view, name='user-profile'),
    path('', profile_view, name='my-profile'),
]
