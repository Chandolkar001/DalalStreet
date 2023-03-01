from django.urls import path, include
from .views import *

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("all-players/", AllPlayerView.as_view(), name="all-players"),
    path("company/", CompanyListView.as_view(), name="company-list"),
    path("IPO/", IPOView.as_view(), name = "ipo"),
    path("IPOSub/", IPOSubscriptionView.as_view(), name="ipo-subs" ),
    path("IPOAddSub/", AddIPOSubscriptionView.as_view(), name="add-ipo-subs" ),
    path("BuyOrders/", BuyOrderView.as_view(),name="buy-orders"),
    path("AddBuyOrders/", AddBuyOrderView.as_view(),name="add-buy-orders"),
    path("SellOrders/", SellOrderView.as_view(),name="sell-orders"),
    path("AddSellOrders/", AddSellOrderView.as_view(),name="sell-orders"),

]