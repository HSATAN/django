#coding=utf-8
import requests
from io import StringIO
from PIL import Image
import re,json
from scrapy.selector import Selector
headers={'Host':'www.dkny.com',
             'Referer':'https://www.dkny.com/us/',
             'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
             'x-requested-with':'XMLHttpRequest'}
url = 'https://cn.calzedonia.com/product/indonesiaboy-shorts/163883.uts'
response=requests.get(url)
sel=Selector(response)
spec = re.findall('var trackingMatrix.+var trackingProductVariantId', str(response.text), re.S)
spec = spec[0].replace('var trackingMatrix =', '').replace('var trackingProductVariantId', '').replace(';','').strip('\n ')
spec = json.loads(spec)
details=''
details_node=spec['variants'][0]['variantComposition']
for detail in details_node:
    if detail['description']:
        details = details + str(detail['percentage']) + detail['description'] + ','
print(details)