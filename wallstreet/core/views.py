from django.shortcuts import render
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import (UserSerializer,IPOSerializer,StockSerializer)
from .models import (User)

class UserRegisterView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class AllPlayerView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

class IPOView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = IPOSerializer
    queryset = User.objects.all()

class StockView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StockSerializer
    queryset = User.objects.all()