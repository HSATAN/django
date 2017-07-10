#coding=utf-8
import requests
from io import StringIO
from PIL import Image
from scrapy.selector import Selector
import re,json
url = 'http://www.panerai.cn/zh-cn/collections/special-editions/2017/luminor-marina-oracle-team-usa-8-days-acciaio--448_pam00724.html'
url='http://weibo.com/gzdaily'
response=requests.get(url=url)
print(response.text)
sel=Selector(response)
category_nodes=sel.xpath('//div[@class="head"]/div[@class="inner"]/div/div//a/@href').extract()

script=sel.xpath('//script[last()]/text()').extract()
script1 = sel.xpath('//script[last()]').extract()
#print(script[0])
#print(script1)
#print(script)
data=re.findall('productDescription".+"productDelivery"',str(script),re.S)


#data=re.findall('productDescription".+"productDelivery"',str(script[0]),re.S)[0].split(':')[1].replace('"productDelivery"','')
#print(data)

spec=re.findall('var trackingMatrix.+var trackingProductVariantId',str(response.text),re.S)
if spec:
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
    #print(len(mycolors))
    #print(mycolors)
    newcolors=set()
    for mmm in mycolors:
        for k,v in mmm.items():
            pass
            #print(k)
            #print(v)
        newcolors.add(mmm['COLOR_NAME'])
    newcolors=list(newcolors)
    #print(newcolors)

    spec=spec['sizeForStoreAvailability']
    specs=[]
    #print(spec)
    for temp_spec  in spec:
        specs.append(temp_spec['sizeName'])
    #print(specs)
else:
    print(sel.xpath('//section[@class="product-features"]').extract())
    spec = re.findall('var trackingMatrix.+var trackingProductVariantId', str(response.text), re.S)
