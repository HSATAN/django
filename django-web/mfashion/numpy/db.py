#_*_ coding:utf-8 _*_
import sys
import pymysql
import logging
import smtplib,time
from email.mime.text import MIMEText
import threading

database_ali={}
database_ali['host']='rm-2zeabe2a02n34m358o.mysql.rds.aliyuncs.com'
database_ali['port']=3306
database_ali['user']='spider'
database_ali['passwd']='Be0jx1KRmK'
database_ali['db']='products_core'
database_ali['charset']='utf8'

conn_ali=pymysql.connect(**database_ali)
ali_cursor=conn_ali.cursor(cursor=pymysql.cursors.DictCursor)
