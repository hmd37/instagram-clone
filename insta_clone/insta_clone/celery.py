import os

from celery import Celery


if os.name == 'nt':  # Only for Windows
    os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insta_clone.settings')

app = Celery('insta_clone')

app.conf.worker_pool = 'solo'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
