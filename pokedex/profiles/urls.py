from django.urls import path
from .views import profile_view, change_avatar, edit_profile, daily_reward, friend_request, accept_friend_request, \
    remove_user_from_friend, show_friends, decline_friend_request

urlpatterns = [
    path('showfriends/', show_friends, name='show_friends'),
    path('editprofile/', edit_profile, name='edit-profile'),
    path('dailyreward/', daily_reward, name='daily-reward'),
    path('editprofile/changeavatar/<int:avatar>/', change_avatar, name='change-avatar'),
    path('<str:username>/', profile_view, name='user-profile'),
    path('', profile_view, name='my-profile'),
    path('friendrequest/<str:username>/<str:friendname>/', friend_request, name='friend-request'),
    path('acceptfriendrequest/<str:friendname>/', accept_friend_request, name='friend-request'),
    path('removefriend/<str:username>/<str:friendname>/', remove_user_from_friend, name='remove-friend'),
    path('declinerequest/<str:friendname>/', decline_friend_request, name='decline-friend'),
]
