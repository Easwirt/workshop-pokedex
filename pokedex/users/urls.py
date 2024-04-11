from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='logout'),
    path('emailverification/<uidb64>/<token>/', views.email_verification, name='confirmationmail'),
]
