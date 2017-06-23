#_*_ coding:utf-8 _*_
from datetime import timedelta
celery_result_backend='redis://47.93.24.159:6379/1'
broker_url='redis://47.93.24.159:6379/0'

celerybeat_schedule={
    'every-5-min':{
        'task':'tasks.spider',
        'schedule':timedelta(seconds=30),
        'args':('weather')

    }
}