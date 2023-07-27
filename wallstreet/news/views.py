from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import News
from .serializers import *

# Create your views here.
class NewsListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = NewsSerializer
    queryset = News.getPublishedNews()

class NewsDetailView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = NewsSerializer
    queryset = News.getPublishedNews()
