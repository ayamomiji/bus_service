import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bus_service.settings")

app = Celery("bus_service")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from bus_notifiers.tasks import check_notifiers

    sender.add_periodic_task(15.0, check_notifiers.s(), name="check notifiers")


app.conf.broker_url = "redis://localhost:6379/0"
app.conf.broker_connection_retry_on_startup = True

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
