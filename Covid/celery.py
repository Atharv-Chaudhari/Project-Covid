import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Covid.settings')

# For settings and all of cloudAMQP
# https://www.cloudamqp.com/docs/celery.html#recommended-settings
# command to install rabbit on local 
# choco install rabbitmq

# Code For CloudAMQP for Heroku
# import os
# # broker_url = os.environ.get('amqps://xwwclfrs:n8Dz-5ooraTsgcmm_Vsu8WzDPYNPHRsx@jackal.rmq.cloudamqp.com/xwwclfrs')
# broker_pool_limit = 1 # Will decrease connection usage
# broker_heartbeat = None # We're using TCP keep-alive instead
# broker_connection_timeout = 30 # May require a long timeout due to Linux DNS timeouts etc
# # result_backend = None # AMQP is not recommended as result backend as it creates thousands of queues
# event_queue_expires = 60 # Will delete all celeryev. queues without consumers after 1 minute.
# worker_prefetch_multiplier = 1 # Disable prefetching, it's causes problems and doesn't help performance
# worker_concurrency = 50 # If you tasks are CPU bound, then limit to the number of cores, otherwise increase substainally
app = Celery('Covid', broker='amqps://xwwclfrs:n8Dz-5ooraTsgcmm_Vsu8WzDPYNPHRsx@jackal.rmq.cloudamqp.com/xwwclfrs')
app.tasks['__main__.sleepy','__main__.send_mail_task','__main__.world_data']
print(app.conf.broker_url)

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