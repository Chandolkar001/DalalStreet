from django.urls import path, include
from .views import *

urlpatterns = [
    path("", NewsListView.as_view(), name="newslist"),
    path("<int:pk>", NewsDetailView.as_view(), name="newsdetail"),
]