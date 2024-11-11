from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notification_Scheduler.settings')

# Create a new instance of Celery 
app = Celery('Notification_Scheduler')


# Load the configuration from the settings file
app.config_from_object('django.conf:settings', namespace='CELERY')


# Auto-discover task modules in all the applications in the Django project
app.autodiscover_tasks()

