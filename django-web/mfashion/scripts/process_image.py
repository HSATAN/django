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

#conn_ali=pymysql.connect(**database_ali)
conn_qinyun=pymysql.connect(**database)
conn_ali=pymysql.connect(**database_ali)
product_image_conn=pymysql.connect(**database)
image_store_conn=pymysql.connect(**database)
image_store_cursor=image_store_conn.cursor(cursor=pymysql.cursors.DictCursor)
product_image_cursor=product_image_conn.cursor(cursor=pymysql.cursors.DictCursor)
qingyun_cursor=conn_qinyun.cursor(cursor=pymysql.cursors.DictCursor)
ali_cursor=conn_ali.cursor(cursor=pymysql.cursors.DictCursor)
logging.basicConfig(level=logging.INFO, format='[line: %(lineno)d]  [time:%(asctime)s]  %(levelname)s :  %(message)s',
                    datefmt='%Y-%m-%d %H:%M', filename='exportToali.log',
                    filemode='w')

def process_image():
    product_image_time='2016-12-29 07:57:09'
    #10049,10057,10135,10149,10152,10184,10220,10226,
    brand_list = [10333,10350,10369,10373,14997]
    for brand_id in brand_list:
        sql_image='select * from products_image WHERE  brand_id="%s"'%(brand_id)
        ali_sql_product = 'select fingerprint from products where brand_id=%s' % brand_id
        ali_sql_image='select fingerprint from products_image where brand_id=%s' % brand_id
        print(sql_image)
        print(ali_sql_image)
        print(ali_sql_product)
        del_fingerprint=[]
        ali_cursor.execute(ali_sql_image)
        image_model_result=ali_cursor.fetchall()
        for image_model in image_model_result:
            del_fingerprint.append(image_model['fingerprint'])
        ali_cursor.execute(ali_sql_product)
        ali_result=ali_cursor.fetchall()
        model_list=[]
        for model_tem in ali_result:
            if model_tem['fingerprint'] not in del_fingerprint:
                model_list.append(model_tem['fingerprint'])
        print(len(model_list))
        model_list=set(model_list)
        print(len(model_list))
        if len(model_list)==0:
            continue
        #time.sleep(5)
        product_image_cursor.execute(sql_image)
        result_image=product_image_cursor.fetchall()
        flag_image = False
        count_products_image=0
        print('+++++++++++++++')
        print(brand_id)
        for result in result_image:
            fingerprint=result['fingerprint']
            if fingerprint in model_list:
                print('+++++++++++++++++++++++')
                #print(result['fingerprint'])
                count_products_image+=1
                image_checksum=result['checksum']
                print(image_checksum)
                sql_store='select * from images_store where checksum="%s"'%(image_checksum)
                print(sql_store)
                image_store_cursor.execute(sql_store)
                result_store=image_store_cursor.fetchall()
                count_images_store=0
                for store in result_store:
                    count_images_store+=1
                    checksum=store['checksum']
                    print('------------------')
                    url=store['url']
                    url_hash=store['url_hash']
                    path=store['path']
                    width=store['width']
                    height=store['height']
                    format=store['format']
                    size=store['size']
                    update_time_store=store['update_time']
                    try:
                        ali_cursor.execute('insert into images_store (checksum,url,url_hash,path,width,height,format,size,update_time) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(checksum,url,url_hash,path,width,height,format,size,update_time_store))
                        idproducts_image = result['idproducts_image']
                        brand = result['brand_id']
                        model = result['model']
                        update_time = result['update_time']
                        rank = result['rank']
                        ali_cursor.execute(
                            'insert into products_image (checksum,brand_id,model,fingerprint,update_time,rank) VALUES ("%s","%s","%s","%s","%s","%s")' % (
                             image_checksum, brand, model, fingerprint, update_time, rank))
                        conn_ali.commit()
                        conn_ali.commit()
                        flag_image=True
                    except Exception as e:
                        print(e)
                        conn_ali.rollback()
                        conn_ali.rollback()
                        if 'duplicate' in str(e).lower():
                            flag_image=True
                        logging.error(str(e))
    return flag_image

if __name__=='__main__':
    process_image()
    conn_ali.close()
    conn_qinyun.close()