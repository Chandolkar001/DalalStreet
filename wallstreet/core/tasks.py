from celery import shared_task
from celery import Celery
from datetime import timedelta
from django.conf import settings
from .utils import to_match
from .models import Market, Company

app = Celery('app')

@app.task
def match_order_task():
    if Market.objects.get(id=1).market_on:
        to_match()
        print("match order executed")
    else:
        print("market is closed")

@app.task
def graph_val():
    if Market.objects.get(id=1).market_on:
        company = Company.objects.all()
        for comp in company:
            comp.last_traded_prices.append(comp.last_traded_price)
            comp.save()
            print("graph val executed")
    else:
        print("Market closed")