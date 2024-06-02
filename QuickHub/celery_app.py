import os
import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QuickHub.settings')

app = celery.Celery('QuickHub')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
# что бы celery ароматически искала нужные таски
app.autodiscover_tasks()
