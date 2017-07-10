#coding=utf-8
import os
import json
import re
from PIL import Image
from io import StringIO
from scrapy.http import FormRequest
from scrapy.selector import Selector
from lxml import etree
import scrapy
class formdata_spider(scrapy.Spider):
    name = 'form'
    allowed_domains=['*']
    def start_requests(self):
        url='http://weibo.com/gzdaily'
        yield scrapy.http.FormRequest(url=url, callback=self.parse)
        #formdata参数的值是存储在request对象的body属性中
    def parse(self, response):
        sel=Selector(response)
        print(response.text)
