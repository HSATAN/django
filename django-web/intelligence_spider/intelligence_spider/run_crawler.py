from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
import sys
sys.path.append(r"D:\django\django-web\intelligence_spider")
from intelligence_spider.spiders.joke_spider  import MySpider as spider
#from intelligence_spider.spiders.test_spider  import TestSpider as spider
from scrapy.utils.project import get_project_settings

crawl=Crawler(spider,get_project_settings())
crawl.signals.connect(reactor.stop,signal=signals.spider_closed)
crawl.crawl()
reactor.run()
