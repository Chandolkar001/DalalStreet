from celery import shared_task
from celery import Celery
from datetime import timedelta
from django.conf import settings
from .utils import to_match
from .models import Market

app = Celery('app')

@app.task
def match_order_task():
    if Market.objects.get(id=1).market_on:
        to_match()
        print("executed")
    else:
        print("market is closed")