from celery import shared_task
from celery import Celery
from datetime import timedelta
from django.conf import settings
from .models import News
from core.models import Market

app = Celery('app')

@app.task
def news_update():
    if Market.objects.get(id=1).market_on:
        news = News.objects.filter(isPublished = False).first()
        news.isPublished = True
        news.save()
        print("news executed")
    else:
        print("market is closed")
