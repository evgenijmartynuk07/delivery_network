import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.delivery_network.settings')

app = Celery('backend.delivery_network')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

