# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

count=1
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        global count
        count+=1
        #print(request.body)