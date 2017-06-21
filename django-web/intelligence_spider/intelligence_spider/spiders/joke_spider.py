#coding=utf-8
import scrapy
from scrapy import Request
from scrapy import Selector
import sys,copy
import os
import json
import re
import datetime
import requests
from lxml import etree
import time
import logging,re,json
#from intelligence_spider.items import IntelligenceImageItem

class MySpider(scrapy.Spider):
    name = 'joke'
    allowed_domains = ['*']
    start_urls = [
        'http://www.weather.com.cn/weather1d/101010100.shtml#search'
    ]
    def parse(self,response):
        print('================')
        #print(response.body.decode('utf-8'))
        sel=Selector(response)
        try:
            temperature_list=sel.xpath('//div[@class="curve_livezs"]/following-sibling::script[1]/text()').extract()[0]
            data=json.loads(re.findall('{.+}',temperature_list)[0])
            print(str(data))
            print(data['1d'])
            print(len(data['1d']))
            print(list(data['1d'])[:6])
        except Exception as e:
            print(e)



