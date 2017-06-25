#_*_ coding:utf-8 _*_
from datetime import timedelta
from celery.schedules import crontab
from kombu import Exchange,Queue
#CELERY_RESULT_BACKEND='redis://47.93.24.159:6379/1'
BROKER_URL='redis://47.93.24.159:6379/1'
CELERY_RESULT_BACKEND='db+mysql://root@127.0.0.1/celery'

'''

CELERY_TASK_RESULT_EXPIRES = 20 * 60  #20 minutes

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'

default_exchange = Exchange('default', type='direct')
media_exchange = Exchange('media', type='direct')

CELERY_QUEUES = (
    #main_cycle用于任务分发，置于中心节点,队列使用main做名称
    Queue('weather', default_exchange, routing_key='weather'),
    #image_download用于图片下载，分发给专门的下载上传节点，队列使用download做名称
    Queue('joke', default_exchange, routing_key='joke')

)


class MyRouter(object):
    def route_for_task(self, task, args=None, kwargs=None):
        if task == 'tasks.jokespider':
            return {
                'routing_key': 'joke'}

        elif task == 'tasks.spider':
            return {
                'routing_key': 'weather'}
        else:
            return None


CELERY_ROUTES = (MyRouter(), )



#使用mysql做结果数据库,
CELERY_RESULT_BACKEND='db+mysql://root@127.0.0.1/celery'#最后celery为数据库的名字
CELERY_RESULT_DB_TABLENAMES = {#设置数据库表
    'task': 'taskmeta',
    'group': 'groupmeta',
}

#设置mongodb做结果数据库
CELERY_RESULT_BACKEND='mongodb'
CELERY_RESULT_BACKEND_SETTINGS={#设置数据库连接配置
    'host':'47.93.5.189',
    'port':27017,
    'database':'spidertask',
    'taskmeta_collection':'spidermeta'
}
'''
CELERYBEAT_SCHEDULE={
    'every-5-min':{
        'task':'tasks.spider',
        'schedule':timedelta(seconds=3600),
        'args':None

    },
    'every-1-min':{
        'task':'tasks.joke_spider',
        'schedule':timedelta(seconds=3600),
        'args':None
    }
}
