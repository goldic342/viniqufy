from celery import Celery

from src import celeryconfig

celery = Celery('tasks')
celery.config_from_object(celeryconfig)
