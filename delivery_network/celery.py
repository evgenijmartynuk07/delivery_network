import os

from celery import Celery

from delivery_network import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_network.settings')

app = Celery('delivery_network')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
