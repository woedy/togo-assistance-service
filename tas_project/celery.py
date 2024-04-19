import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tas_project.settings')
app = Celery('tas_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()