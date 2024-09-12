from celery import Celery

from src.config import CeleryConfig

celery = Celery('tasks')
celery.config_from_object(CeleryConfig)
