from celery import Celery

app=Celery('wether',broker='amqp://guest@localhost//')
@app.task()
def hello(name):
    return 'hello '+name