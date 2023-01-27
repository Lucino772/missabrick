import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'missabrick.settings')

celery = Celery('missabrick')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.conf.broker_url = os.getenv('MISSABRICK_CELERY_BROKER_URL')
celery.autodiscover_tasks()
