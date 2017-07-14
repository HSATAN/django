#coding=utf8
from scrapy_redis.spiders import RedisSpider

class MyRSpider(RedisSpider):
    name = 'redis_spider'
    def parse(self, response):
        print(response.text)
        pass