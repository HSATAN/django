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

    def start_requests(self):
        metadata = {'region': 'us', 'category': []}

        start_urls =['https://www.fendi.com/us']

        for url in start_urls:

            # self.fix_cookie(url)
            m = copy.deepcopy(metadata)
            if m['region'] == 'cn' or m['region']=='it':
                log.msg('--------------------------')
                yield Request(
                    url=url,
                    meta={'userdata': m},
                    callback=self.parse_cn,
                    errback=self.onerr
                )
            else:
                yield Request(
                    url=url,
                    meta={'userdata': m},
                    callback=self.parse
                )

    def parse(self,response):
        sel=Selector(response)
        metadata=response.meta['userdata']
        if metadata['region']=='cn':
            urls=['http://www.fendi.cn/女士产品系列','http://www.fendi.cn/男士产品系列']
            for url in urls:
                m=copy.deepcopy(metadata)
                if '女士' in url:
                    m['gender']='2'
                elif '男士' in url:
                    m['gender']='1'
                yield Request(url=url, meta={'userdata': m}, callback=self.parse_gender_cn,
                              dont_filter=True)

        else:
            nodes=sel.xpath('//ul[@data-mainmenu-items="> li"]//li[@role="menuitem"]')
            level_1=[]
            for node in nodes:
                if 'http' in node.xpath("./a//@href").extract()[0]:
                    continue
                level_1.append('https://www.fendi.com'+node.xpath("./a//@href").extract()[0])
                self.handlurl.add('https://www.fendi.com'+node.xpath("./a//@href").extract()[0])
            print(self.handlurl)
            level_1=copy.deepcopy(self.handlurl)
            for url in level_1:
                m = copy.deepcopy(metadata)
                if 'woman'  in url:
                    m['gender'] = '2'
                elif 'man' in url:
                    m['gender'] = '1'
                elif 'boy' in url:
                    m['gender'] = '4'
                elif 'girl' in url:
                    m['gender'] = '5'
                elif 'baby' in url:
                    m['gender'] = '6'

                if 'beauty' in url or 'fragrance' in url or 'make-up' in url or '/beauty-gifts/' in url:
                    m['category'] = ['fragrances']

                if 'clothing' in url or 'read-ro-wear' in url or 'shop-by-look' in url:
                    m['category'] = ['clothes']
                elif 'bags' in url or 'small-leather-goods' in url or 'Kan-I' in url or 'peekaboo' in url or 'urban-attitude' in url or 'selleria' in url:
                    m['category'] = ['bags']
                elif 'scarves' in url or 'strap' in url or 'fashion' in url or 'belts' in url or 'ABC' in url or 'sunglasses' in url or 'accessories' in url or 'book' in url:
                    m['category'] = ['accessories']
                elif 'shoes' in url:
                    m['category'] = ['shoes']
                elif 'timepieces' in url or 'momento' in url or 'crazy-carats' in url or 'policromia' in url or 'watch' in url:
                    m['category']=['watches']
                print(len(self.handlurl))
                yield Request(url=url, meta={'userdata': m}, callback=self.parse_url_list,
                              dont_filter=True)
    def parse_url_list(self,response):
        sel = Selector(response)
        metadata = response.meta['userdata']
        urls=[]
        load_more=sel.xpath('//div[@class="load-more-container"]')
        if not load_more:
            urls=sel.xpath('//div[@data-carousel-setclasses="false"]//meta[@itemprop="url"]//@content').extract()
        else:
            sel = Selector(response)
            m=copy.deepcopy(metadata)
            url=response.url+'?q=:relevance&page=10&preload=true'
            yield Request(url=url, meta={'userdata': m}, callback=self.parse_load_more,
                              dont_filter=True)
        self.prox_set = self.prox_set | set(urls)
        print(len(self.prox_set))
        if self.flag==0 and len(self.prox_set)>750:
            self.flag=1
            for url in self.prox_set:
                m = copy.deepcopy(metadata)
                yield Request(url=url, meta={'userdata': m}, callback=self.parse_detail,
                 dont_filter=True)

    def parse_load_more(self,response):
        sel = Selector(response)
        metadata = response.meta['userdata']
        urls = sel.xpath('//div[@data-carousel-setclasses="false"]//meta[@itemprop="url"]//@content').extract()
        self.prox_set=self.prox_set|set(urls)
        print(len(self.prox_set))
        if self.flag==0 and len(self.prox_set)>750:
            self.flag = 1
            for url in self.prox_set:
                m = copy.deepcopy(metadata)
                yield Request(url=url, meta={'userdata': m}, callback=self.parse_detail,
                 dont_filter=True)

        #for url in urls:
            #m = copy.deepcopy(metadata)

            #yield Request(url=url, meta={'userdata': m}, callback=self.parse_detail,
                          #dont_filter=True)

    def parse_detail(self,response):
        print('=================')
        sel = Selector(response)
        metadata = response.meta['userdata']
        name=sel.xpath('//div[@class="product-description"]//h1[@itemprop="name"]//text()').extract()
        if name:
            metadata['name']=name[0]
        else:
            metadata['name']=''
        price=sel.xpath('//div[@class="product-description"]//div[@class="prices js-price-update"]//span/text()').extract()
        model=sel.xpath('//span[@itemprop="productID"]//text()').extract()[0]
        desc=sel.xpath('//p[@itemprop="description"]//text()').extract()
        details_node=sel.xpath('//div[@id="more-details"]//li')

        colors_node=sel.xpath('//div[@class="product-info"]//meta[@itemprop="color"]/@content').extract()
        if colors_node:
            colors_node=colors_node[0]
        else:
            colors_node=''
        colors=''
        for color in colors_node.split(','):
            if 'multicolor' in color.strip(' '):
                continue
            if not colors:
                colors=color.strip(' ')
            else:
                colors=colors+'/'+color.strip(' ')
        metadata['color']=[colors]
        details=''
        for index,detail in enumerate(details_node):
            if index==0:
                continue
            try:
                temp=detail.xpath('.//strong//text()').extract()[0]
                temp=temp+detail.xpath('.//span//text()').extract()[0]
                if not details:
                    details=temp
                else:
                    details=details+','+temp
            except:pass
        imgs=sel.xpath('//div[contains(@class,"item nav-item ")]//img/@data-src').extract()
        metadata['price_discount']=0
        if desc:
            metadata['description']=desc[0]
        else:
            metadata['description']=''
        metadata['details']=details
        if not metadata['category']:
            desc_brief=''
            try:
                desc_brief=sel.xpath('//div[@class="product-description"]//p[@class="product-description"]//text()').extract()[0]
            except:
                desc_brief=''
                pass
            finally:
                metadata['category']=self.get_special_category((str(metadata['name'])+str(desc_brief)).lower())
                pass

        if price:
            price=price[0].strip('\n ')

        metadata['price'] = price
        metadata['model']=model
        metadata['url']=response.url
        print(metadata)

proxies_set = set()
def get_proxies():
    global proxies_set
    proxies_set_file = "proxies_set"
    if len(proxies_set) < 5:
        if os.path.exists(proxies_set_file):
            proxies_set = eval(open(proxies_set_file, "r").read())
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
        url = "http://www.xicidaili.com/nn/"
        url2 = "http://www.xdaili.cn/ipagent//freeip/getFreeIps"
        try:
            r = requests.get(url, headers=headers)
            status_code = r.status_code
            if status_code == 503:
                r = requests.get(url2, headers=headers)
                info_json = json.loads(r.text)
                for data_host in info_json['rows']:
                    proxies_set.add(str.format("{0}:{1}", data_host['ip'], data_host['port']))
            else:
                page = etree.HTML(r.text)
                for host, port in zip(page.xpath("//tr[@class='odd']/td[2]/text()"), page.xpath("//tr[@class='odd']/td[3]/text()")):
                    proxies_set.add(str.format("{0}:{1}", host, port))
        except Exception as  e:
            logging.error('get_proxies error:{0}: {1}'.format(Exception, e))


        # r = requests.get("http://api.xicidaili.com/free2016.txt")
        # for line in r.text.split("\n"):
        #     proxies_set.add(line.strip())
canuse=set()
def test_prox():
    for proxy in proxies_set:
        try:
            proxy='http://'+proxy
            text=requests.get('http://ip.filefab.com/index.php',proxies={'http':proxy},timeout=10).text
            sel=Selector(text=text)
            node=sel.xpath('//h1[@id="ipd"]//text()').extract()
            if node:
                canuse.add(proxy)
        except:pass
get_proxies()
print(canuse)
