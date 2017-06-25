from celery import Celery
import subprocess
app=Celery()
app.config_from_object('celeryconfig')
@app.task()
def spider():
    crawl = subprocess.Popen("scrapy crawl weather", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    crawl.communicate()
    return 'run  '+'wether'

@app.task()
def joke_spider():
    crawl=subprocess.Popen("scrapy crawl joke",stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    crawl.communicate()
    return 'run joke'
