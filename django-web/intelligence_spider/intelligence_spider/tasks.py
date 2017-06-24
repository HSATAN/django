from celery import Celery
import subprocess
app=Celery()
app.config_from_object('config')
@app.task()
def spider(name):
    crawl = subprocess.Popen("scrapy crawl %s" % spider, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    crawl.communicate()
    return 'run  '+name