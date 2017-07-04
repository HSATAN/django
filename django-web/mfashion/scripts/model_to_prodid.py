#_*_ coding:utf-8 _*_
import sys
import pymysql
import logging
import smtplib,time
from email.mime.text import MIMEText
import threading
database={}
database['port']=3306
database['host']='121.201.8.91'
database['user']='rose'
database['passwd']='rose123'
database['db']='products_core'
database['charset']='utf8'


database_ali={}
database_ali['host']='rm-2zeabe2a02n34m358o.mysql.rds.aliyuncs.com'
database_ali['port']=3306
database_ali['user']='spider'
database_ali['passwd']='Be0jx1KRmK'
database_ali['db']='products_core'
database_ali['charset']='utf8'

conn_ali=pymysql.connect(**database_ali)
ali_cursor=conn_ali.cursor(cursor=pymysql.cursors.DictCursor)

def getresult():
    sql='select DISTINCT model from products WHERE prodid IS NULL limit 20000'
    ali_cursor.execute(sql)
    results=ali_cursor.fetchall()

    while results:
        for result in results:
            try:
                model=result['model']
                print(model)
                ali_cursor.execute('update products set prodid="%s" WHERE model="%s"'%(model,model))
                conn_ali.commit()
            except Exception as e:
                print(e)
        sql = 'select DISTINCT model from products WHERE prodid IS NULL limit 20000'
        ali_cursor.execute(sql)
        results = ali_cursor.fetchall()
    ali_cursor.close()
    conn_ali.close()
if '__main__'==__name__:
    getresult()