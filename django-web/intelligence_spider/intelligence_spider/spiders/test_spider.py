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

class TestSpider(scrapy.Spider):
    name = 'joke'
    start_urls = [
        'https://www.rimowa.com/en-ie/',
    ]
    metadata = {'region': 'de', 'brand_id': 1111,
                'tags_mapping': {}, 'category': []}
    def parse(self,response):
        sel=Selector(response)
        node=sel.xpath('//span[@class="products_cont" or @id="products_cont"]//span//a/@href').extract()
        for url in node:
            print(url)
            yield Request(url=url,callback=self.parse_list,meta={"userdata":self.metadata})

    def parse_list(self,response):
        sel=Selector(response)
        metadata=response.meta['userdata']
        urls=sel.xpath('//ul[@class="active"]//li//a/@href').extract()
        for url in urls:
            m=copy.deepcopy(metadata)
            print(url)
            yield Request(url=url,callback=self.parse_detail,meta={'userdata':m})
    def parse_detail(self,response):
        sel=Selector(response)
        metadata=response.meta['userdata']
        metadata['url']=response.url
        model=response.url.split('/')[-1]
        metadata['model']=model
        name=sel.xpath('//span[@class="title-product"]/text()').extract()
        if name:
            metadata['name']=name[0].strip('\n\r\t ')
        desc=sel.xpath('//table[@class="details"]//tr//td/text()').extract()
        if desc:
            metadata['description']=','.join(desc).strip('\n\r\t, ')
        prifix_image='https://www.rimowa.com/media/products/924.63.03.5/rotation/03.png'
        images=[]
        for i in range(1,9):
            images.append('https://www.rimowa.com/media/products/%s/rotation/%s.png'%(model,str(i).zfill(2)))
        price=re.findall('price_raw":(.*?),',response.text,re.S)
        if price:
            metadata['price']=price[0].strip('" ')+'€'
        print(price)
        print(response.url)
        print(images)
        print(metadata)

