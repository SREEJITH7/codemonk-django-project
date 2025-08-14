import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")  # change 'project' to your settings module name

app = Celery("codemonk")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
