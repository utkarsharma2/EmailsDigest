import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Server.settings')
app = Celery('Server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')