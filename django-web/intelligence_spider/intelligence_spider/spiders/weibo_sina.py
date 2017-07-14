#coding=utf-8
import scrapy
from scrapy.selector import Selector
class sina_spider(scrapy.Spider):
    name='sina'
    start_urls=['http://weibo.com/']
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
             'Host':'weibo.com',
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-Encoding':'gzip, deflate, sdch',
             'Accept-Language':'zh-CN,zh;q=0.8',
             'Upgrade-Insecure-Requests':'1'}
    def start_requests(self):
        url='http://weibo.com/'
        yield scrapy.Request(url=url,callback=self.parse)
    def parse(self, response):
        print(response.request)
        print(response.text)