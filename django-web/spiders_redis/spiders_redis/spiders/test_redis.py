#coding=utf8
from scrapy_redis.spiders import RedisSpider

class MyRSpider(RedisSpider):
    name = 'myspider'
    def parse(self, response):
        print(response.text)
        pass