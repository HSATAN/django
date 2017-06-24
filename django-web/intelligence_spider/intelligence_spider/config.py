#_*_ coding:utf-8 _*_
from datetime import timedelta
from celery.schedules import crontab
#CELERY_RESULT_BACKEND='redis://47.93.24.159:6379/1'
BROKER_URL='redis://47.93.24.159:6379/1'
CELERY_RESULT_BACKEND='mongodb'
CELERY_RESULT_BACKEND_SETTINGS={
    'host':'47.93.5.189',
    'port':27017,
    'database':'spidertask',
    'taskmeta_collection':'spidermeta'
}
CELERYBEAT_SCHEDULE={
    'every-5-min':{
        'task':'tasks.spider',
        'schedule':timedelta(seconds=60),
        'args':None

    }
}