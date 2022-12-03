from django.urls import path, include
from .views import (UserRegisterView, AllPlayerView)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("all-players/", AllPlayerView.as_view(), name="all-players")
]