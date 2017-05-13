# -*- coding:utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import Selector
from scrapy import log
import sys,copy
import os
import json
import re
import datetime
import requests
from lxml import etree
import logging
import time
#from intelligence_spider.items import IntelligenceImageItem

class MySpider(scrapy.Spider):
    name = 'joke'
    allowed_domains = ['*']
    start_urls = [
        'https://www.fendi.com/us'
    ]
    def __init__(self):
        global proxies_set
        self.prox_set=proxies_set
        self.total=0
        self.seen=set()
        self.flag=0
        self.handlurl=set()
    def parse(self,response):
        sel=Selector(response)
        metadata=response.meta['userdata']

