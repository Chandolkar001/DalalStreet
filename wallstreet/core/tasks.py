from celery import shared_task
from celery import Celery
from datetime import timedelta
from django.conf import settings
from .utils import match_orders

@shared_task
def match_order_task():
    match_orders()

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'match_order-every-10-minutes': {
        'task': 'core.tasks.match_order_task',
        'schedule': timedelta(seconds=10),
    },
}