import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Covid.settings')

# For settings and all of cloudAMQP
# https://www.cloudamqp.com/docs/celery.html#recommended-settings
# command to install rabbit on local 
# choco install rabbitmq

# Code For CloudAMQP for Heroku

app = Celery('Covid')

# app = Celery('Covid')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')