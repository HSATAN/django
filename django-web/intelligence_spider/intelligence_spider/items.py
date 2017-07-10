# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class IntelligenceWeatherItem(scrapy.Item):
    weather=scrapy.Field()
class ImageItem(scrapy.Item):
    images=scrapy.Field()
    images_url=scrapy.Field()
class FileItem(scrapy.Item):
    files=scrapy.Field()
    files_url=scrapy.Field()
