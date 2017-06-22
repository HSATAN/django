from celery import Celery

app=Celery('wether',broker='redis://47.93.24.159:6379/0',backend='redis://47.93.24.159:6379/0')
@app.task()
def hello(name):
    return 'hello '+name