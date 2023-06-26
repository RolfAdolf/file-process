from celery import Celery

import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_process.settings")

app = Celery("file_process")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
