from celery import Celery

from config import CeleryConfig

celery = Celery("tasks")
celery.config_from_object(CeleryConfig)
