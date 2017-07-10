#coding=utf-8
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import sys
'''运行良好'''
sys.path.append(r"D:\django\django-web\intelligence_spider")
from intelligence_spider.items import ImageItem
class Image_Spider(scrapy.Spider):
    name = 'image'
    start_urls=['http://www.ivsky.com/']
    def parse(self, response):
        sel=Selector(response)
        urls=sel.xpath('//img//@src').extract()
        item=ImageItem()
        item['images_url']=urls
        yield item