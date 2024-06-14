from django.urls import path
from .views import *

urlpatterns = [
    path('editprofile/', edit_profile, name='edit-profile'),
    path('dailyreward/', daily_reward, name='daily-reward'),
    path('editprofile/changeavatar/<int:avatar>/', change_avatar, name='change-avatar'),
    path('editprofile/clearrecentactivity/', clear_recent_activity, name='clear-recent-activity'),
    path('editprofile/changepassword/<str:old_password>/<str:new_password1>/<str:new_password2>/', change_password, name='change-password'),
    path('editprofile/updatebio/<str:new_bio>/', update_bio, name='update-bio'),
    path('editprofile/updateprivacy/', update_privacy, name='update-privacy'),
    path('<str:username>/', profile_view, name='user-profile'),
    path('', profile_view, name='my-profile'),
    path('friendrequest/<str:username>/<str:friendname>/', friend_request, name='friend-request'),
    path('acceptfriendrequest/<str:username>/<str:friendname>/', accept_friend_request, name='friend-request'),
    path('removefriend/<str:username>/<str:friendname>/', remove_user_from_friend, name='remove-friend'),
]
