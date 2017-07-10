#coding=utf-8

'''
运行良好
'''
from scrapy.http import Request
import scrapy
from scrapy.selector import Selector
from intelligence_spider.items import FileItem
class file_spider(scrapy.Spider):
    name = 'file'
    start_urls=['http://vdisk.weibo.com/s/aVI9cTPV7QfVe']
    def parse(self, response):
        sel=Selector(response)
        files_url=['http://116.242.0.143/file3.data.weipan.cn/84118909/69644df8f7b66560b4d3d5bb70e6ac679961479a?ip=1499703839,36.102.227.180&ssig=St8Bvgwj6u&Expires=1499704439&KID=sae,l30zoo1wmz&fn=数字图像处理第三版中文版.pdf&skiprd=2&se_ip_debug=36.102.227.180&corp=2&from=1221134&wsiphost=ipdb']
        item=FileItem()
        item['files_url']=files_url
        yield item