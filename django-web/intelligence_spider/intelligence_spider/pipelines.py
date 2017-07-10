# -*- coding: utf-8 -*-
import sys
import time
import scrapy
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from matplotlib.pyplot import plot,savefig
import numpy as np
import datetime
import re,os
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
#sys.path.append(r"D:django-git\django\django-web\intelligence_spider")
from intelligence_spider.db.connMongo import handleMongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class IntelligenceWeatherPipeline(object):
    def __init__(self):
        self.client=handleMongo.get_mongo()
        self.db=self.client['weather']
        self.conn=self.db['beijing']
    def process_item(self, item, spider):
        date_weather=str(datetime.datetime.now().strftime('%Y-%m-%d'))
        update_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result=self.conn.update({'_id':date_weather},{'$set':{'weather':item['weather'],'update_time':update_time}},True)
        self.client.close()
        day=[]
        temperature=[]
        for data in item['weather']:
            day.append(re.findall('[0-9]+',data)[1])
            temperature.append(re.findall('[0-9]+',data)[3])

        numpy_day=np.array(day)
        numpy_temperature=np.array(temperature)
        print(numpy_day)
        print(numpy_temperature)
        plot(numpy_day,numpy_temperature,'--*b')
        path=os.getcwd()
        path=path.split('django-web')[0]
        path=path+'django-web'+'/machinelearning/static/weatherpic'+'/'+date_weather+'.jpg'
        if not os.path.exists(path):
            savefig(path)
        return item
    def close_spider(self,spider):
        pass

class MyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['images_url']:
            yield scrapy.Request(image_url)
    def item_completed(self, results, item, info):
        for end in results:
            end[1]['path']=end[1]['path'].split('/')[0]+'/'+str(time.time())
            print(end)
        return item

class MyFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['files_url']:
            yield scrapy.Request(image_url)
    def item_completed(self, results, item, info):
        return item