# -*- coding:utf-8 -*-

import sys
import os
import json
import re
import datetime
import requests
from lxml import etree
import logging
import time

__author__ = 'liuzhuang'
__date__ = '2015-10-29'

#---------------------------------LOG-------------------------------------------------

LOGGING_FILE = 'kuaidi_db.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=LOGGING_FILE,
    filemode='a+'
)

#--------------------------------国际快递URL--------------------------------------------

PORT78 = "http://port78.com/query.php"
ANL = "http://www.anlexpress.com/?ship200trackingtool=ship200-trackingtool"
COLISSIMO = "http://www.colissimo.fr/portail_colissimo/suivre.do?language=en_GB"
FLYING_PARCEL = "http://www.flyingparcel.net/tracking.aspx"
QUICK_SHIP = "http://www.qk-ship.com/cgi-bin/GInfo.dll?EmmisTrack"
XYNYC = "http://www.xynyc.com/SelectNum.aspx?send={0}"
XLOBO = "http://m.xlobo.com/Api/BillQuery/GetBillTrackInfo"
SURETON = "http://www.sureton.com/index.php/Index/exp_track"
VALUEWAY = "http://member.valueway.net/cgi-bin/GInfo.dll?EmmisTrack"
THE1EX = "http://www.the1ex.com/TrackSearch.aspx?TXT_TRACKNO={0}"
MAYIMA = "http://www.mayima.net/cgi-bin/GInfo.dll?EmmisTrack"

#--------------------------------快递100URL----------------------------------------------

KUAIDI100 = "http://www.kuaidi100.com/query?type={0}&postid={1}"
KDCX = "http://www.kdcx.cn/index.php?r=site/query&nu={0}"

#----------------------------------快递信息初始化-------------------------------------------
def init_express_info(param):
    express_info = dict()
    express_info['data'] = []
    express_info['package_no'] = param['package_no']
    #express_info['transport_company'] = param['transport_company']
    return express_info


#----------------------------------获取HTML源码----------------------------------------------
def get_html(url, post_data, headers):

    times = 0
    logging.debug('request to href: {0}'.format(url))
    while times < 3:
        try:
            r = requests.post(url=url, data=post_data, headers=headers, timeout=30)
            return r.text
        except  :
            times += 1
            time.sleep(0.02)
            #get_html(url, post_data, headers)
    logging.debug("{0} response is none".format(url))
    return ""



#----------------------------------THE1EX-------------------------------------------------

def get_the1ex_transport_info(param):
    html = get_html(THE1EX.format(param.get("package_no")), {}, {})

    express_info = ""
    if not html:
        logging.error('the1ex response is blank for href:{0}'.format(THE1EX))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("//div[@class='commnTxt']/table/tr")

    express_info = init_express_info(param)
    if not nodes:
        express_info = json.dumps(express_info)
        return express_info

    express_info["transport_state"] = "0"
    express_info["transport_company"] = "the1ex"

    for node in nodes[1:]:

        time = node.xpath("./td[1]/text()")
        status = node.xpath("./td[2]/text()")
        operate_user = node.xpath("./td[3]/text()")
        express_no = node.xpath("./td[2]/a/text()")

        if time:
            t_str = time[0].encode('utf-8')
            t_time = datetime.datetime.strptime(t_str, "%Y/%m/%d %H:%M:%S")
            update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            update_time = ""

        if status and operate_user:
            if not express_no:
                context = str.format("状态:{0},录入人:{1}", status[0].encode('utf-8'), operate_user[0].encode('utf-8'))
            else:
                context = str.format("状态:{0},单号:{1},录入人:{2}", status[0].encode("utf-8"),
                                     express_no[0].encode("utf-8"), operate_user[0].encode("utf-8"))
        elif status and not operate_user:
            if not express_no:
                context = str.format("状态:{0}", status[0].encode('utf-8'))
            else:
                context = str.format("状态:{0},单号:{1}", status[0].encode("utf-8"), express_no[0].encode("utf-8"))
        else:
            context = ""

        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "国内转运"
        if keywords in context:
            express_info['transport_state'] = "3"

    express_info = json.dumps(express_info)
    return express_info


#----------------------------------PORT78-------------------------------------------------
def get_port78_transport_info(param):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
    post_data = {"send": 2, "orderid": param['package_no']}

    express_info = ""
    html = get_html(PORT78, post_data, headers)
    if not html:
        logging.error('port78 response is blank for href:{0}'.format(PORT78))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("//div[@class='IDCon clr']/table/tr")

    express_info = init_express_info(param)
    if not nodes:
        express_info = json.dumps(express_info)
        return express_info

    express_info['transport_state'] = "0"
    express_info['transport_company'] = "port78"

    for node in nodes[1:]:
        no = node.xpath("./td[1]/p")
        status = node.xpath("./td[2]/p")
        location = node.xpath("./td[3]/p")
        update_time = node.xpath("./td[4]/p")

        if update_time:
            t_str = update_time[0].text.split(',')[1].encode('utf-8')  #过滤掉星期几
            try:
                t_time = datetime.datetime.strptime(t_str, " %Y年%m月%d日 %H点%M分")
                update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")
            except  :
                update_time = ''
                logging.error("日期格式不符,{0}".format(e))
        else:
            update_time = ''

        if status and location:
            context = str.format("状态:{0},地点:{1}", status[0].text.encode('utf-8'), location[0].text.encode('utf-8'))
        elif status and not location:
            context = str.format("状态:{0}", status[0].text.encode('utf-8'))
        elif not status and location:
            context = str.format("地点:{1}", location[0].text.encode('utf-8'))
        else:
            context = ''

        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "清关完毕"
        if keywords in context:
            express_info['transport_state'] = "3"
    express_info = json.dumps(express_info)
    return express_info


#----------------------------------ANL-------------------------------------------------
def get_anl_transport_info(param):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
    post_data = {"Tracking": param['package_no']}

    express_info = ""
    html = get_html(ANL, post_data, headers=headers)
    if not html:
        logging.error('ANL response is blank for href:{0}'.format(ANL))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("//div[@id='ship200apiResponse']/p[1]/text()")

    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "anl"

    for node in nodes:
        node = node.strip("\r\n").strip(" ")

        if "Not Found" in node:
            express_info = json.dumps(express_info)
            return express_info

        if "-" not in node:
            continue

        if node and (node is not ''):
            status = node.split("-")
            t_str = status[0].encode('utf-8').strip(" ")
            t_time = datetime.datetime.strptime(t_str, "%m/%d/%Y")
            update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")

            context = status[1].split("/")[0].encode('utf-8').strip(" ")

            express_info['data'].append({'time': update_time, 'context': context})

            keywords = "已签收"
            if keywords in context:
                express_info['transport_state'] = "3"
    express_info = json.dumps(express_info)
    return express_info


#----------------------------------COLISSIMO-------------------------------------------
def get_colissimo_transport_info(param):

    post_data = {'parcelnumber': param['package_no']}

    express_info = ""
    html = get_html(COLISSIMO, post_data, {})
    if not html:
        logging.error('COLISSIMO response is blank for href:{0}'.format(COLISSIMO))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("//table[@class='dataArray']/tbody/tr")

    if not nodes:
        return express_info

    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "colissimo"
    for node in nodes:
        Date = node.xpath("./td[1]/text()")
        Libelle = node.xpath("./td[2]/text()")
        site = node.xpath("./td[3]/text()")

        if Date:
            t_str = Date[0].encode('utf-8')
            t_time = datetime.datetime.strptime(t_str, "%d/%m/%Y")
            update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            update_time = ""

        Libelle = Libelle[0].encode('utf-8')
        site = site[0].encode('utf-8').strip()
        context = str.format("Libelle:{0}; Localisation:{1}",Libelle, site)

        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "签收"
        if keywords in context:
            express_info['transport_state'] = "3"  #国际快递完成
    express_info = json.dumps(express_info)
    return express_info


#----------------------------------FlyingParcel----------------------------------------
def get_flyingparcel_transport_info(param):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
    post_data = {"yundanno": param['package_no']}

    express_info = ""
    html = get_html(FLYING_PARCEL, post_data, headers)
    if not html:
        logging.error('FlyingParcel response is blank for href:{0}'.format(FLYING_PARCEL))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("/html/body/table/tr[3]/td/table/td[3]/table/tr[3]/td/table/span/tr/td/table/tr")

    if len(nodes) <= 1:
        return express_info

    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "flyingparcel"

    for node in nodes[1:]:
        t_str = node.xpath("./td[1]/text()")
        status = node.xpath("./td[2]/b/text()")
        if t_str:
            t_str = t_str[0].encode('utf-8')
            if ":" not in t_str:
                t_time = datetime.datetime.strptime(t_str, "%Y/%m/%d")
            else:
                t_time = datetime.datetime.strptime(t_str, "%Y/%m/%d %H:%M:%S")
            # t_str = re.findall(r"(\d+)/(\d+)/(\d+).*?", t_str)
            # t_time = datetime.datetime(int(t_str[0][0]), int(t_str[0][1]), int(t_str[0][2]))
            update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            update_time = ""

        if status:
            context = status[0].encode('utf-8').strip("\n").strip("\t")
        else:
            context = ""

        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "国内快递配送中"
        if keywords in context:
            express_info['transport_state'] = "3"  #国际快递
    express_info = json.dumps(express_info)
    return express_info


#----------------------------------QuickShip------------------------------------------
def get_quickship_transport_info(param):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
    post_data = {"cno": param['package_no']}

    express_info = ""
    html = get_html(QUICK_SHIP, post_data, headers)
    if not html:
        logging.error('QUICKSHIP response is blank for href:{0}'.format(QUICK_SHIP))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("//div[@id='zmainContent']//div[@id='oDetail']/table/tr")

    if not nodes:
        return express_info

    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "quickship"

    for node in nodes[1:]:
        oHDateTime = node.xpath("./td[1]/text()")
        oHPlace = node.xpath("./td[2]/text()")
        oHDetail = node.xpath("./td[3]/text()")

        update_time = oHDateTime[0].encode('utf-8')
        context = str.format("服务地点:{0};详细内容:{1}",oHPlace[0].encode('utf-8'), oHDetail[0].encode('utf-8'))

        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "已签收"
        if keywords in context:
            express_info['transport_state'] = "3"  #国际快递完成
    express_info = json.dumps(express_info)
    return express_info


#----------------------------------SURETON----------------------------------------------
def get_sureton_transport_info(param):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
    post_data = {"exp_no": param['package_no']}

    express_info = ""
    html = get_html(SURETON, post_data, headers)
    if not html:
        logging.error('SUERTON response is blank for href:{0}'.format(SURETON))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("/html/body/table[5]/tr/td/table/tr")

    express_info = init_express_info(param)

    if not nodes:
        express_info = json.dumps(express_info)
        return express_info

    for node in nodes[1:]:
        detail_nodes = node.xpath("./td/table/tbody/tr")
        if not detail_nodes:
            express_info = json.dumps(express_info)
            return express_info

        express_info['transport_state'] = "0"
        express_info['transport_company'] = "sureton"
        for detail_node in detail_nodes:
            t_str = detail_node.xpath("./td[1]/text()")
            status = detail_node.xpath("./td[2]/text()")

            update_time = t_str[0].encode('utf-8')
            context = status[0].encode('utf-8')

            keywords = "海关清关"
            if keywords in context:
                express_info['transport_state'] = "3"

            express_info['data'].append({'time': update_time, 'context': context})
    express_info = json.dumps(express_info)
    return express_info



#----------------------------------VALUEWAY--------------------------------------------
def get_valueway_transport_info(param):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
    post_data = {"cno": param['package_no']}

    express_info = ""
    html = get_html(VALUEWAY, post_data, headers)
    if not html:
        logging.error('VALUEWAY response is blank for href:{0}'.format(VALUEWAY))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("//div[@id='oDetail']/table/tr[@align='center']")

    if not nodes:
        return express_info

    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "valueway"
    for node in nodes:
        oHDateTime = node.xpath("./td[1]/text()")
        oHPlace = node.xpath("./td[2]/text()")
        oHDetail = node.xpath("./td[3]/text()")

        if oHDateTime:
            t_str = oHDateTime[0].encode('utf-8')
            t_time = datetime.datetime.strptime(t_str, "%Y-%m-%d %H:%M")
            update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            update_time = ""

        context = str.format("服务网点:{0};详细内容:{1}",oHPlace[0].encode('utf-8').strip(" "), oHDetail[0].encode('utf-8'))

        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "签收"
        if keywords in context:
            express_info['transport_state'] = "3"
    express_info = json.dumps(express_info)
    return express_info


#-----------------------------------XLOBO------------------------------------------------
def get_xlobo_transport_info(param):

    post_data = {"billCode": param['package_no']}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
               "Referer": "http://www.xlobo.com/Public/QueryBill.aspx?code={0}".format(param['package_no']),
               "Host": "www.xlobo.com"}

    express_info = ""
    html = get_html(XLOBO, post_data, headers={})

    if not html:
        logging.error('XLOBO response is blank for href:{0}'.format(XLOBO))
        return express_info

    info_json = json.loads(html)

    if not info_json.get("IsSuccess"):
        return express_info
    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "xlobo"
    nodes = info_json.get("Result").get('Status')

    for node in nodes[::-1]:
        operate_time = node.get("OperationDateTime")
        operator = node.get("Operator")
        status = node.get("Status")

        context = str.format("状态:{0};{1}", operator.encode("utf-8"), status.encode("utf-8"))

        express_info['data'].append({'time': operate_time.encode("utf-8"), 'context': context})

        keywords = "国内"
        if keywords in context:
            express_info['transport_state'] = "3"

    express_info = json.dumps(express_info)
    return express_info

#-----------------------------------XYNYC-------------------------------------------------
def get_xynyc_transport_info(param):

    url = XYNYC.format(param['package_no'])

    express_info = ""
    html = get_html(url, {}, {})
    if not html:
        logging.error('XYNYC response is blank for href:{0}'.format(XYNYC))
        return express_info

    html = re.sub("&nbsp;", " ", html)
    page = etree.HTML(html)
    nodes = page.xpath("//div[@class='con-cb']/ul/li/span[2]/text()")

    if not nodes:
        return express_info

    if "未找到相关信息" in nodes[0].encode('utf-8'):
        return express_info

    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "xynyc"

    for node in nodes:
        node = node.encode('utf-8')
        node = node.split(" ")
        if len(node) < 2:
            continue

        t_str = " ".join([node[0], node[1]])

        try:
            t_time = datetime.datetime.strptime(t_str, "%Y年%m月%d日 %H:%M:%S")
        except ValueError:
            t_time = datetime.datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S")
        update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")

        context = " ".join(node[2:])

        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "签收人"
        if keywords in context:
            express_info['transport_state'] = "3"  #国际快递完成

    express_info = json.dumps(express_info)
    return express_info


#---------------------------------MAYIMA----------------------------------------------
def get_mayima_transport_info(param):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
               "Referer": "http://www.mayima.net/"}

    post_data = {"w": "mayima", "cno": param['package_no']}

    express_info = ""
    html = get_html(MAYIMA, post_data, headers)
    if not html:
        logging.error('MAYIMA response is blank for href:{0}'.format(MAYIMA))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("//div[@id='oDetail']/table/tr[@align='center']")
    if not nodes:
        return express_info

    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "MAYIMA"

    for node in nodes:
        oHDateTime = node.xpath("./td[1]/text()")
        oHPlace = node.xpath("./td[2]/text()")
        oHDetail = node.xpath("./td[3]/text()")

        if oHDateTime:
            t_str = oHDateTime[0].encode('utf-8') if isinstance(oHDateTime[0], unicode) else oHDateTime[0]
            try:
                t_time = datetime.datetime.strptime(t_str.replace("/", "-"), "%Y-%m-%d %H:%M")
            except ValueError:
                t_time = datetime.datetime.strptime(t_str.replace("/", "-"), "%Y-%m-%d")
            update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            update_time = ""

        service_place = oHPlace[0].encode('utf-8').strip() if isinstance(oHPlace[0], unicode) else oHPlace[0]
        detail = oHDetail[0].encode('utf-8') if isinstance(oHDetail[0], unicode) else oHDetail[0]

        context = str.format("服务地点:{0};详细内容:{1}", service_place, detail)

        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "签收"
        if keywords in context:
            express_info['transport_state'] = "3"

    express_info = json.dumps(express_info)
    return express_info


#---------------------------------安达美亚----------------------------------------------
def get_andameiya_transport_info(param):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
               "Referer": "http://andameiya.com/"}
    url = str.format("http://andameiya.com/Home/Index/waybillQuery.html?sn={0}", param['package_no'])
    express_info = ""
    try:
        res = requests.get(url, headers=headers, timeout=30)
        html = res.text
    except:
        html = ""
    if not html:
        logging.error('response is blank for href:{0}'.format(url))
        return express_info

    page = etree.HTML(html)
    nodes = page.xpath("//div[@class='table-responsive']/table/tbody/tr")
    if not nodes:
        return express_info

    express_info = init_express_info(param)
    express_info['transport_state'] = "0"
    express_info['transport_company'] = "安达美亚"

    for node in nodes[1:]:
        oHDateTime = node.xpath("./td[1]/text()")
        oHDetail = node.xpath("./td[2]/text()")

        update_time = ""
        if oHDateTime:
            t_str = oHDateTime[0].encode('utf-8') if isinstance(oHDateTime[0], unicode) else oHDateTime[0]
            try:
                t_time = datetime.datetime.strptime(t_str.replace("/", "-"), "%Y-%m-%d %H:%M")
                update_time = t_time.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass

        detail = oHDetail[0].encode('utf-8') if isinstance(oHDetail[0], unicode) else oHDetail[0]
        context = str.format("{0}", detail.strip())
        express_info['data'].append({'time': update_time, 'context': context})

        keywords = "签收"
        if keywords in context:
            express_info['transport_state'] = "3"

    express_info = json.dumps(express_info)
    return express_info


def format_time(time_str):
    if time_str == "":
        return time_str

    if len(time_str) < 19:
        return time_str

    if int(time_str[11:13]) >= 24:
        hour = str(int(time_str[11:13]) - 12)
        ctime_str = time_str[0:11] + hour + time_str[13:]
    else:
        ctime_str = time_str
    time_date = datetime.datetime.strptime(ctime_str, "%Y-%m-%d %H:%M:%S")
    return time_date.strftime("%Y-%m-%d %H:%M:%S")


#-----------------------------KUAIDI100--------------------------------------------
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
        except  :
            logging.error('get_proxies error:{0}: {1}'.format( ))


        # r = requests.get("http://api.xicidaili.com/free2016.txt")
        # for line in r.text.split("\n"):
        #     proxies_set.add(line.strip())
    open(proxies_set_file, "w").write(str(proxies_set))
    return proxies_set.pop()

def add_proxies(proxie):
    proxies_set.add(proxie)

def remove_proxies(proxie):
    if proxie in proxies_set:
        proxies_set.remove(proxie)

kuaidi_list = set()
def load_kuaidi_list():
    global kuaidi_list
    for line in open("kuaidi_list.conf", "r"):
        arrs = line.strip().split("\t")
        kuaidi_list.add(arrs[0])
load_kuaidi_list()

def format_time(time_str):
    if time_str == "":
        return time_str

    if len(time_str) < 19:
        return time_str

    if int(time_str[11:13]) >= 24:
        hour = str(int(time_str[11:13]) - 12)
        ctime_str = time_str[0:11] + hour + time_str[13:]
    else:
        ctime_str = time_str
    time_date = datetime.datetime.strptime(ctime_str, "%Y-%m-%d %H:%M:%S")
    return time_date.strftime("%Y-%m-%d %H:%M:%S")

def get_kuaidi100_transport_info(param):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/39.0.2171.95 Safari/537.36",
        "Referer": "http://www.kuaidi100.com/"
    }
    proxie = get_proxies()
    proxies = {"http": str.format("http://{0}", proxie)}

    express_info = ""
    href = KUAIDI100.format(param['transport_code'], param['package_no'])
    logging.debug('request to href: {0}'.format(href))
    logging.debug('proxie: {0}\tproxie count:{1}'.format(proxie, len(proxies_set)))
    try:
        resp = requests.get(href, proxies=proxies, headers=headers, timeout=10)
    except  :
        if len(proxies_set)>5:
            remove_proxies(proxie)
            return get_kuaidi100_transport_info(param)
        logging.error('kuaidi100 requests error:{0}: {1}'.format( ))
        return express_info

    if resp.text:
        try:
            info_json = json.loads(resp.text)
        except ValueError:
            if len(proxies_set)>5:
                remove_proxies(proxie)
                return get_kuaidi100_transport_info(param)
            logging.error('kuaidi100 loads response json error:{0}'.format(resp.text))
            return express_info
        
        add_proxies(proxie)
        if info_json.get('status', '') == '200':
            transport_company = info_json.get('com', '')
            tmp_dict = dict()
            tmp_dict['package_no'] = info_json.get('nu', '')
            tmp_dict['transport_company'] = transport_company
            # print info_json
            # tmp_dict['transport_state'] = check_trans_state()
            
            tmp_dict['transport_state']=0

            tmp_dict['data'] = []
            for data in info_json.get('data', ''):
                time_str = format_time(data.get('time', ''))
                if check_trans_state(data['context']):
                    tmp_dict['transport_state'] = 3
                tmp_dict['data'].append(
                    {
                        'time': time_str,
                        'context': data.get('context', '')
                    }
                )
            express_info = json.dumps(tmp_dict)
        else:
            if info_json.get('status', '') == '604':
                remove_proxies(proxie)
            logging.error('kuai100 response json wrong:{0}'.format(info_json))
    else:
        logging.error('kuaidi100 response is blank for href:{0}'.format(href))

    if express_info == "" and param['transport_code'].lower() == "ems":
        suffix = param['package_no'][-2:].lower()
        with open("./kuaidi.conf", "r") as conffile:
            conf = json.loads(conffile.read())
            suffix_map = conf["suffix_map"]
        if suffix in suffix_map:
            param = {"package_no": param['package_no'], 'transport_code': suffix_map[suffix]}
            return get_kuaidi100_transport_info(param)

    return express_info

def get_kdcx_transport_info(param):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/39.0.2171.95 Safari/537.36",
        "Referer": "http://www.kuaidi100.com/"
    }
    proxie = get_proxies()
    proxies = {"http": str.format("http://{0}", proxie)}

    express_info = ""
    href = KDCX.format(param['package_no'])
    logging.debug('request to href: {0}'.format(href))
    logging.debug('proxie: {0}\tproxie count:{1}'.format(proxie, len(proxies_set)))
    # print 'proxie: {0}\tproxie count:{1}'.format(proxie, len(proxies_set))
    try:
        resp = requests.get(href, proxies=proxies, headers=headers, timeout=10)
    except  :
        if len(proxies_set)>5:
            remove_proxies(proxie)
            return get_kdcx_transport_info(param)
        # print 'KDXC requests error:{0}: {1}'.format( )
        logging.error('KDXC requests error:{0}: {1}'.format( ))
        return express_info
    # print resp.text
    if resp.text:
        try:
            info_json = json.loads(resp.text)
        except ValueError:
            if len(proxies_set)>5:
                remove_proxies(proxie)
                # return get_kdcx_transport_info(param)
            logging.error('KDXC loads response json error:{0}'.format(resp.text))
            return express_info

        add_proxies(proxie)
        if info_json['success']:
            transport_company = info_json['company']
            tmp_dict = dict()
            tmp_dict['package_no'] = info_json.get('nu', '')
            tmp_dict['transport_company'] = transport_company
            if 6==info_json.get('status', ''):
                tmp_dict['transport_state'] = 3
            else:
                tmp_dict['transport_state']=0

            tmp_dict['data'] = []
            for data in info_json.get('data', ''):
                time_str = format_time(data.get('time', ''))
                tmp_dict['data'].append(
                    {
                        'time': time_str,
                        'context': data.get('context', '')
                    }
                )
            express_info = json.dumps(tmp_dict)
        else:
            logging.error('kdcx response json wrong:{0}'.format(info_json))
    else:
        logging.error('kdcx response is blank for href:{0}'.format(href))
    return express_info
#-----------------------------函数映射---------------------------------------

def transport_function_mapping(param):

    transport_mapping = {
        "valueway": get_valueway_transport_info,
        "sureton": get_sureton_transport_info,
        # "xlobo": get_xlobo_transport_info,
        "xynyc": get_xynyc_transport_info,
        "quickship": get_quickship_transport_info,
        "flyingparcel": get_flyingparcel_transport_info,
        # "colissimo": get_colissimo_transport_info,
        "anl": get_anl_transport_info,
        "port78": get_port78_transport_info,
        "the1ex": get_the1ex_transport_info,
        "MAYIMA": get_mayima_transport_info,
        "安达美亚": get_andameiya_transport_info,
    }

    #如果快递公司编码和包裹号不存在,返回
    express_info = ''
    if (not param['transport_code']) and (not param['package_no']):
        return express_info, 0

    #快递公司编码不在国际快递中,快递100查询
    company_list = [transport_code for transport_code, function in transport_mapping.items()]
    if param['transport_code'] in company_list:
        express_info = transport_mapping[str(param['transport_code'])](param)
        return express_info, 1
    elif param['transport_code'] in kuaidi_list:
        return get_kuaidi100_transport_info(param), 2
    elif re.match(r'^[A-Z]{2}[0-9]{9}[A-Z]{2}$',param['package_no'],re.M|re.I):
        param['transport_code']='ems'
        return get_kuaidi100_transport_info(param), 2
    else:
        ret = get_kdcx_transport_info(param)
        return ret, 3 

def check_trans_state(context):
    if "签收" in context:
        return 3
    elif "送达" in context:
        return 3
    else:
        return 0
def main():
    #param = {"package_no": "T701081", 'transport_code': 'the1ex','transport_company': 'the1ex'}
    #param = {"package_no": "8800004020", 'transport_code': 'port78','transport_company': 'port78'}
    #param = {"package_no": "90001036626", 'transport_code': 'anl', 'transport_company': 'anl'}
    #param = {"package_no": "EY022096354FR", 'transport_code': 'colissimo', 'transport_company': 'colissimo'}
    #param = {"package_no": "FPS2011394CA", 'transport_code': 'flyingparcel' ,'transport_company': 'flyingparcel'}
    #param = {"package_no": "1018904415", 'transport_code': 'quickship', 'transport_company': 'quickship'}
    #param = {"package_no": "DB003204138FR", 'transport_code': 'xlobo', 'transport_company': 'xlobo'}
    #param = {"package_no": "DB846876796CA", 'transport_code': 'valueway', 'transport_company': 'valueway'}
    #param = {"package_no": "STE100107930YVR", 'transport_code': 'surton', 'transport_company': 'sureton'}
    #param = {"package_no": "XY00092095", 'transport_code': 'xynyc', 'transport_company': 'xynyc'}
    #param = {"package_no": "880350384879600241", "transport_code": "yuantong", "transport_company":"圆通"}
    #param = {"package_no": "M000438833JP", "transport_code": "mayima", "transport_company": "mayima"}
    param = {"package_no": "308302670933", "transport_code": "PF", "transport_company": "日本邮政"}
    print (transport_function_mapping(param))

if __name__ == '__main__':
    main()


