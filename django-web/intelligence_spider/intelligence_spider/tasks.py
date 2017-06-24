from celery import Celery
import subprocess
app=Celery()
app.config_from_object('config')
@app.task()
def spider():
    crawl = subprocess.Popen("scrapy crawl weather", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    crawl.communicate()
    return 'run  '+'wether'