#_*_ coding:utf-8 _*_
from datetime import timedelta
CELERY_RESULT_BACKEND='redis://47.93.24.159:6379/1'
BROKER_URL='redis://47.93.24.159:6379/0'

CELERYBEAT_SCHEDULE={
    'every-5-min':{
        'task':'tasks.spider',
        'schedule':timedelta(seconds=30),
        'args':('weather')

    }
}