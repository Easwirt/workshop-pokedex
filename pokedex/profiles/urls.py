from django.urls import path
from .views import profile_view, change_avatar, edit_profile


urlpatterns = [
    path('', profile_view, name='my-profile'),
    path('<str:username>/', profile_view, name='user-profile'),
    path('changeavatar/<int:avatar>/', change_avatar, name='change-avatar'),
]
