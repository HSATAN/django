import smtplib
from email.mime.text import MIMEText
import sys
import pymysql
import logging

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

#conn_ali=pymysql.connect(**database_ali)
conn_qinyun=pymysql.connect(**database)
conn_ali=pymysql.connect(**database_ali)
product_image_conn=pymysql.connect(**database)
image_store_conn=pymysql.connect(**database)
image_store_cursor=image_store_conn.cursor(cursor=pymysql.cursors.DictCursor)
product_image_cursor=product_image_conn.cursor(cursor=pymysql.cursors.DictCursor)
qingyun_cursor=conn_qinyun.cursor(cursor=pymysql.cursors.DictCursor)
ali_cursor=conn_ali.cursor(cursor=pymysql.cursors.DictCursor)

def sendemail(data):
    msg = MIMEText(data, _subtype='html', _charset='utf-8')
    # msg = MIMEMultipart('alternative')
    msg['Subject'] = u'数据迁移到阿里云'
    msg['From'] = 'huagnkaijie <kaijie.huang@mfashion.com.cn>'
    msg['To'] = '2499090390@qq.com'

    server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
    server.login('buddy@mfashion.com.cn', 'rose123')
    server.sendmail('buddy@mfashion.com.cn',['2499090390@qq.com'], msg.as_string())
    server.quit()
sendemail('====================')
def get_update_time():
    brand_list=[10029,10030,10049,10057,10058,10066,10070,10074,10076,10079,10084,10093,10106,10109,10135,
    10142,10149,10150,10152,10166,10178,10184,10192,10212,10220,10226,10239,10248,10259,10263,10264,10268,10270,10300,
    10308,10316,10322,10333,10350,10354,10367,10369,10373,10385,10388,10429,10510,10669,10856,10897,10946,11301,11614,13084,13902,
    14022,14097,14162,14163,14997]
    for brand in brand_list:
        try:
            update_time_sql='SELECT * FROM products_core.images_store where path like "'+str(brand)+ "%" '"and update_time>"2016-12-29 07:57:09" order by update_time asc limit 1'
            print(brand)
            print(update_time_sql)
            update_time=image_store_cursor.execute(update_time_sql)
            result=image_store_cursor.fetchone()
            print(result['update_time'])
        except Exception as e:
            print(e)
    conn_ali.close()
    conn_qinyun.close()
#get_update_time()

