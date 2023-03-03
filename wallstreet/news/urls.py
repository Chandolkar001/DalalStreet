from django.urls import path, include
from .views import *

urlpatterns = [
    path("", NewsListView.as_view(), name="newslist"),
]