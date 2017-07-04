#coding=utf-8
import os
import json
import re
from PIL import Image
from io import StringIO
from scrapy.http import FormRequest
from scrapy.selector import Selector
from lxml import etree
import scrapy
class formdata_spider(scrapy.Spider):
    name = 'form'
    allowed_domains=['*']
    def start_requests(self):
        url = 'http://www.panerai.cn/zh-cn/home.html'
        url='http://www.panerai.cn/zh-cn/collections/watch-collection/luminor-1950.html'
        yield scrapy.http.FormRequest(url=url, callback=self.parse)
        #formdata参数的值是存储在request对象的body属性中
    def parse(self, response):
        sel=Selector(response)
        category_nodes=sel.xpath('//div[@class="head"]/div[@class="inner"]/div/div//a/@href').extract()
        print(category_nodes)
        print(response.text)

        script=sel.xpath('//script[last()]/text()').extract()
        script1 = sel.xpath('//script[last()]').extract()
        #print(script[0])
        #print(script1)
        data=re.findall('productDescription".+"productDelivery"',str(script))[0].split(':')[1].replace('"productDelivery"','')
        #print(data)

        spec=re.findall('var trackingMatrix.+var trackingProductVariantId',str(response.text),re.S)
        spec=spec[0].replace('var trackingMatrix =','').replace('var trackingProductVariantId','').replace(';','').strip('\n ')
        print(spec)
        spec=json.loads(spec)
        #print(spec)
        #for k,v in spec.items():
            #print(k)

            #print(v)
        #print(type(spec))
        #print(spec['variants'])
        mycolors=spec['variants']
        print(len(mycolors))
        print(mycolors)
        newcolors=set()
        for mmm in mycolors:
            for k,v in mmm.items():
                pass
                print(k)
                print(v)
            newcolors.add(mmm['COLOR_NAME'])
        newcolors=list(newcolors)
        #print(newcolors)

        spec=spec['sizeForStoreAvailability']
        specs=[]
        #print(spec)
        for temp_spec  in spec:
            specs.append(temp_spec['sizeCode'])
        print(specs)
        #print(response.text)

        '''

        buf=StringIO(response.body)
        buf.seek(0)
        orig_imag=Image.open(buf)
        orig_imag.load()
        with open('test.png','wb') as  f:
            f.write(response.body)
        # yield Request(method=)
        '''
        url='http://www.panerai.cn/zh-cn/collections/special-editions/2017/luminor-marina-oracle-team-usa-8-days-acciaio--448_pam00724.html'
        #yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True)
    def parse_list(self,response):
        sel=Selector(response)
        #page=etree.HTML(str(response.body))
        print(response.text)
        color=sel.xpath('//dl[@itemprop="description"]//dd[last()]/text()').extract()
        color=list(set(color))
        print(color)
        print(len(color))
        name=sel.xpath('//div[@class="h1" and @itemprop="name"]//text()').extract()
        names=''
        if name:
            for name_tem in name:
                if name_tem.strip('\n '):
                    names=names+name_tem
        else:
            us_name=re.findall('class="h1" itemprop="name">(.+?)<nav class="inlin',str(response.body))
            if us_name:
                print(us_name)
        details=sel.xpath('//div[@class="mobile-height-calc"]//text()').extract()
        re_details=re.findall('<b>.{1,5}</b>.+?</p>',str(response.text))
        final_details=''
        for detail_tem in re_details:
            title=re.findall('<b>(.+?)</b>',detail_tem)[0]
            context=re.findall('</b>(.+?)</p>',detail_tem)[0].strip('。., ')
            final_details=final_details+title+': '+context+','
            #print(title)
            #print(context)
        print(final_details)
        us_color=re.findall('<dt>Dial color</dt>(.+?)</dd>',str(response.body))
        if us_color:
            us_color=us_color[0]
            us_color=re.findall('<dd>(.+)',us_color)
        print(us_color)
        id=model=re.findall('productID">(.+?)</h2>',str(response.body))
        print(id)


        image_urls=re.findall('ul class="scroll">(.*?)</ul>',response.text,re.S)
        image1=re.findall('<img src="(.+?)"',image_urls[0],re.S)
        image2=re.findall('background-image: url\(/(.+?)\)',image_urls[0],re.S)
        image2.append(image1[0].lstrip('/'))
        final_images=[]
        for image in image2:
            image=image.replace('880.521','1333.2000')
            final_images.append('http://www.panerai.cn/'+image)
        final_images=list(set(final_images))
        #print(details)
        #print(final_details)
        #print(names)
        #print(re_details)
        print(final_images)
