from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wallstreet.settings')
app = Celery('wallstreet')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'match_order_task': {
        'task': 'core.tasks.match_order_task',
        'schedule': crontab(minute='*/15'),
    },
    'graph_val': {
        'task': 'core.tasks.graph_val',
        'schedule': crontab(minute='*/20'),
    },
    'news_update': {
        'task': 'news.tasks.news_update',
        'schedule': crontab(minute='*/15'),
    },
}