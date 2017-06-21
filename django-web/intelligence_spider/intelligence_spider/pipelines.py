# -*- coding: utf-8 -*-
import sys
import scrapy
import datetime
#sys.path.append('D:\django-web\intelligence_spider\intelligence_spider')
from db.connMongo import handleMongo
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
        return item
    def close_spider(self,spider):
        pass
