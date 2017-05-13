import sys
import os
import json
import re
import datetime
import requests
from lxml import etree
import logging
import time
proxies_set=set()
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
        except  :
            logging.error('get_proxies error:{0}: {1}'.format( ))


        # r = requests.get("http://api.xicidaili.com/free2016.txt")
        # for line in r.text.split("\n"):
        #     proxies_set.add(line.strip())
    open(proxies_set_file, "w").write(str(proxies_set))
    return proxies_set.pop()
print(get_proxies())