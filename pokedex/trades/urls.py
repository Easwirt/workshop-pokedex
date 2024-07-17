from django.urls import path
from .views import *

urlpatterns = [
    path('tradeList/<str:friendname>/', trade_list, name='tradeList'),
    path('saveTrade/', save_trade, name='saveTrade'),
    path('showTrade/', show_trade, name='showTrade'),
    path('acceptTrade/', accept_trade, name='acceptTrade'),
]
