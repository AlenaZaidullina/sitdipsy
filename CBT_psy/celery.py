import os
from celery import Celery

# дефолтные настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CBT_psy.settings')

app = Celery('CBT_psy')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач из всех зарегистрированных Django apps
app.autodiscover_tasks()