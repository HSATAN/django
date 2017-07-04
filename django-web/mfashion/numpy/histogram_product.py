#_*_ coding:utf-8 _*_
import scrapy
from matplotlib import pyplot
import os
import numpy
import sys
import pymysql
import logging
import smtplib,time
from email.mime.text import MIMEText
import threading
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)


database_ali={}
database_ali['host']='rm-2zeabe2a02n34m358o.mysql.rds.aliyuncs.com'
database_ali['port']=3306
database_ali['user']='spider'
database_ali['passwd']='Be0jx1KRmK'
database_ali['db']='products_core'
database_ali['charset']='utf8'

conn_ali=pymysql.connect(**database_ali)
ali_cursor=conn_ali.cursor(cursor=pymysql.cursors.DictCursor)


def get_brand_sum():
    sql='select brand_id ,count(*) as brand_count from products group by brand_id'
    ali_cursor.execute(sql)
    results=ali_cursor.fetchall()
    ali_cursor.close()
    conn_ali.close()
    brand=[]
    brand_count=[]
    for result in results:
        brand.append(result['brand_id'])
        brand_count.append(result['brand_count'])

    print(brand_count)
    print(brand)
    #brand=numpy.array(brand)
    #brand_count=numpy.array(brand_count)
    print(brand)
    print(brand_count)
    pyplot.bar(range(1,len(brand_count)+1),brand_count,linewidth=2,linestyle='-',hatch='/',tick_label=brand,label='a')
    pyplot.subplots_adjust(wspace=8)
    pyplot.legend()
    pyplot.xlabel('品牌id',fontproperties=font_set)
    pyplot.ylabel('商品数量',fontproperties=font_set)
    pyplot.title('品牌数量直方图',fontproperties=font_set)
    pyplot.grid()
    pyplot.show()

    print(numpy.max(brand_count))
    print(numpy.min(brand_count))
    print(numpy.max(brand ))
    print(numpy.min(brand ))

if __name__=="__main__":
    get_brand_sum()