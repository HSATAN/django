#coding=utf8
import requests
from bs4 import BeautifulSoup

url='http://acm.hit.edu.cn/hoj/system/login'
pastdata={
    'username':'HSATAN',
    'password':'shequ1234'

}
se=requests.post(url,data=pastdata)
print(se.content)