from celery import shared_task
from celery import Celery
from datetime import timedelta
from django.conf import settings
from .utils import match_orders

app = Celery('app')

@app.task
def match_order_task():
    match_orders()