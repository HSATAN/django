# -*- coding: utf-8 -*-
import sys
import scrapy
sys.path.append('D:\django-web\intelligence_spider\intelligence_spider')
from db.connMongo import handleMongo
from scrapy.contrib.pipeline.images import ImagesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class IntelligenceImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)
    def item_completed(self, results, item, info):
        return item
class IntelligenceSpiderPipeline(object):
    def __init__(self):
        self.client=handleMongo.get_mongo()
        self.db=self.client['runnoob']
        self.conn=self.db['qiubai']
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    def process_item(self, item, spider):
        print('---------------------------------------------------------------')
        self.conn.insert(item)
        return item
