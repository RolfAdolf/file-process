from celery import Celery
from django.conf import settings

import os


if settings.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_process.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_process.settings.local")

app = Celery("file_process")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
