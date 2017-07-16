#coding=utf8
from scrapy_redis.spiders import RedisSpider

class MyRSpider(RedisSpider):
    name = 'myspider'
    redis_key = 'myspider:test'
    def parse(self, response):
        print(response.text)
        pass