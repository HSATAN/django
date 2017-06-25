#_*_ coding:utf-8 _*_
from datetime import timedelta
from celery.schedules import crontab
from kombu import Exchange,Queue
#CELERY_RESULT_BACKEND='redis://47.93.24.159:6379/1'
BROKER_URL='redis://47.93.24.159:6379/1'
CELERY_RESULT_BACKEND='db+mysql://root@127.0.0.1/celery'
'''
CELERY_RESULT_BACKEND='mongodb'
CELERY_RESULT_BACKEND_SETTINGS={
    'host':'47.93.5.189',
    'port':27017,
    'database':'spidertask',
    'taskmeta_collection':'spidermeta'
}
'''
CELERYBEAT_SCHEDULE={
    'every-5-min':{
        'task':'tasks.spider',
        'schedule':timedelta(seconds=60),
        'args':None

    },
    'every-1-min':{
        'task':'tasks.joke_spider',
        'schedule':timedelta(seconds=50),
        'args':None
    }
}


CELERY_DEFAULT_QUEUE="default"
CELERY_DEFAULT_EXCHANGE_TYPE='direct'
CELERY_DEFAULT_ROUTING_KEY='default'

default_exchange=Exchange('default',type='direct')

CELERY_QUEUES=(
    Queue('default',default_exchange,routing_key='default'),
    Queue('weather',default_exchange,routing_key='weather'),
    Queue('joke',default_exchange,routing_key='joke')
)

class MyRouter(object):
    def route_for_task(self,task,args=None,kwargs=None):
        if task=='tasks.spider':
            return {
                'routing_key':'weather'
            }
        elif  task=='tasks.joke_spider':
            return {
                'routing_key':'joke'
            }
        else:return None
