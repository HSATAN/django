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
    allowed_domains = ['*']
    start_urls = [
        'https://www.fendi.com/us/monster-cube-charm-charm-in-red-and-black-fur/p-7AR3866OQF05IP'
    ]
    def parse(self,response):
        print('================')
