import os

import celery.signals
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitcoin_monitor.settings')

app = Celery('bitcoin_monitor')

# Using a string here means the workers don't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    A task that dumps out its own request information.
    To test the worker, do:

    from bitcoin_monitor.celery import debug_task
    debug_task.delay()
    """
    print('Request: {0!r}'.format(self.request))
    return True


@celery.signals.setup_logging.connect
def setup_logging(**kwargs):
    """
    This dummy function is needed to make sure Celery
    doesn't hijack our logger.
    """
    pass
