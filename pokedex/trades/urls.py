from django.urls import path
from .views import *

urlpatterns = [
    path('tradeList/<str:friendname>/', trade_list, name='tradeList'),
]
