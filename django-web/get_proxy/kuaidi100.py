#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import pydevd
# pydevd.settrace('127.0.0.1', port=55555, stdoutToServer=True, stderrToServer=True)

import time
import datetime
import json

import requests
# import MySQLdb

import logging

from kuaidi import *


URL_CODE = 'http://123.59.12.73/internal_service/get_transport_company_code'
URL_KUAIDI = 'http://123.59.12.73/internal_service/get_trade_logistics_info?count=30000'
EXPIRED_TIME = 2*60*60  # 单位秒
REQUEST_DELAY_TIME = 25
LOGGING_FILE = 'kuaidi_db.log'


# win 平台 unicode encode error 问题
import sys
reload(sys)
sys.setdefaultencoding('utf8')


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=LOGGING_FILE,
    filemode='a+'
)


def get_need_update_list():
    """
    获取符合条件 需要查询的订单信息
    :param con:
    :return: [{}, {}, ...]
    """
    results = []
    try:
        r = requests.get(URL_KUAIDI)
        if r.status_code == 200:
            results = r.json()["original"]["data"]
    except Exception, e:
        msg = str.format("{0} : {1}", Exception, str(e))
        logging.warning(msg)
    logging.debug('already get need update list')

    list_ = []
    count = 0
    with open("./kuaidi.conf", "r") as conffile:
        conf = json.loads(conffile.read())
        process_count = conf["process_count"]
        process_num = conf["process_num"]

    company_code_dict = get_company_code_dict()

    for line in results:
        id = int(line['id'])
        trade_no = line['trade_no']
        package_no = line['package_no']
        transport_company = line['transport_company']
        update_time = datetime.datetime.strptime(line['update_time'], "%Y-%m-%d %H:%M:%S")
        trade_status = line['trade_status']
        transport_status = line['transport_status']
        if id % process_count != process_num:
            logging.warning('not targe: id: {0} process: [{1}/{2}]'.format(id, process_num, process_count))
            continue

        if not re.match(r'^[\w ]+$', package_no):
            logging.warning('package_no is invalid for id: {0} {1}'.format(id, package_no))
            continue

        if transport_company and transport_company in company_code_dict:
            transport_code = company_code_dict[transport_company]
        else:
            logging.warning('transport_company is invalid for id: {0} {1}'.format(id, transport_company))
            continue
        if (datetime.datetime.now() - update_time).days == 0 \
                and (datetime.datetime.now() - update_time).seconds < EXPIRED_TIME:
            continue

        if transport_status == 1 or trade_status != 4:
            logging.info('SIGNED id: {0}'.format(id))
            continue

        line_ = {'id': id, 'trade_no': trade_no, 'package_no': package_no, 'transport_code': transport_code,
                 'update_time': update_time}
        logging.info('need update id: {0} {1}'.format(count, id))
        count += 1
        list_.append(line_)
    logging.debug('already fixed need_update_list')

    return list_


def get_company_code_dict():
    """
    快递公司名称 与 快递公司代码 映射关系
    """
    company_code_dict = {}
    try:
        r = requests.get(URL_CODE)
        if r.status_code == 200:
            rjson = r.json()
            for each in rjson["original"]["data"]:
                company_code_dict[each['name_c']] = each['name_e']
    except Exception, e:
        msg = str.format("{0} : {1}", Exception, str(e))
        logging.warning(msg)
    return company_code_dict


def clear_log_file_every_week():
    """
    每周一 上午 清空日志文件
    :return:
    """
    if datetime.datetime.now().weekday() == 0:
        with file(LOGGING_FILE, 'w') as f:
            pass


def main():
    # return
    logging.info('--------------------------- STARTING GET INFO ----------------------------')
    while True:
        clear_log_file_every_week()
        need_list = get_need_update_list()
        logging.debug('main - get need_update_list')

        headers = {'content-type': 'application/json'}
        url = 'http://123.59.12.73/internal_service/transport_info/updateTransportInfo'
        # url = 'http://moses.ofashion.com.cn/internal_service/transport_info/updateTransportInfo'

        total = len(need_list)
        cur_index = 0
        for line in need_list:
            id = line['id']
            trade_no = line['trade_no']
            logging.debug('trying update: {1}-{2} id: {3} trade_no:{0}'.format(trade_no, total, cur_index, id))
            cur_index += 1
            transport_detail, methord = transport_function_mapping(line)

            if trade_no:
                logging.debug('updating id: {1} trade_no: {0}'.format(trade_no, id))
                data = {"trade_id": id, "trade_no": trade_no, "transport_detail": transport_detail}
                try:
                    r = requests.post(url, data=json.dumps(data), headers=headers)
                    if r.status_code == 200:
                        rjson = r.json()
                        if rjson['original']['status'] == 'success':
                            logging.debug('updated result {0}'.format(rjson))
                            logging.debug('updated {0} {1}'.format(id, transport_detail))
                        else:
                            logging.error('updated failed: {0}'.format(rjson))
                            logging.debug('updated {0} {1}'.format(id, transport_detail))
                    else:
                        logging.error('updated failed return code: {0}'.format(r.status_code))

                except Exception, e:
                    logging.error('updated failed: {0}: {1}'.format(Exception, e))
            if methord == 0:
                REQUEST_DELAY_TIME = 0
            elif methord == 1:
                REQUEST_DELAY_TIME = 1
            else:
                REQUEST_DELAY_TIME = 3
            logging.info('---------- {0} seconds -----------------------------------------\n'.format(REQUEST_DELAY_TIME))
            time.sleep(REQUEST_DELAY_TIME)
        time.sleep(600)

def main2():
    print "main ======== 2"

    headers = {'content-type': 'application/json'}
    url = 'http://123.59.12.73/internal_service/transport_info/updateTransportInfo'
    # url = 'http://moses.ofashion.com.cn/internal_service/transport_info/updateTransportInfo'

    line={}
    line['id']='430915'
    line['trade_no']='01170211234406000056'
    line['package_no']='308302670933'
    line['transport_code']='ems'
    id = line['id']
    trade_no = line['trade_no']
    
    transport_detail, methord = transport_function_mapping(line)

    if trade_no:
        logging.debug('updating id: {1} trade_no: {0}'.format(trade_no, id))
        data = {"trade_id": id, "trade_no": trade_no, "transport_detail": transport_detail}
        print data
        try:
            r = requests.post(url, data=json.dumps(data), headers=headers)
            if r.status_code == 200:
                rjson = r.json()
                if rjson['original']['status'] == 'success':
                    logging.debug('updated result {0}'.format(rjson))
                    logging.debug('updated {0} {1}'.format(id, transport_detail))
                else:
                    logging.error('updated failed: {0}'.format(rjson))
                    logging.debug('updated {0} {1}'.format(id, transport_detail))
            else:
                logging.error('updated failed return code: {0}'.format(r.status_code))

        except Exception, e:
            logging.error('updated failed: {0}: {1}'.format(Exception, e))
    if methord == 0:
        REQUEST_DELAY_TIME = 0
    elif methord == 1:
        REQUEST_DELAY_TIME = 1
    else:
        REQUEST_DELAY_TIME = 3
    logging.info('---------- {0} seconds -----------------------------------------\n'.format(REQUEST_DELAY_TIME))
    
    

if __name__ == '__main__':
    # main()
    main2()
