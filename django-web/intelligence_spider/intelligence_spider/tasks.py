from celery import Celery

app=Celery('wether')
app.config_from_object('config')
@app.task()
def hello(name):
    return 'hello '+name