
from __future__ import absolute_import, unicode_literals
import os

# set the default Django settings module for the 'celery' program.
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axf_VUE.settings')

app = Celery('axf_VUE')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.update(
CELERYBEAT_SCHEDULE = {
    "send_msg": {
        "task": "axf_VUE.users.tasks.send_msg",  #执行的函数
        "schedule": crontab(minute="*/1"),   # every minute 每分钟执行
        "args": (3,4)  # # 任务函数参数
    }
}
)


