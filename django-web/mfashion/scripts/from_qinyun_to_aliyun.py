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
global_result=[]
def get_result(qinyun_sql):
    global global_result
    qingyun_cursor.execute(qinyun_sql)
    global_result = qingyun_cursor.fetchall()
    pass
def get_qinyun(brand_id):
    global success_sum
    global fail_sum
    global get_sum
    global global_result
    try:
        count=1
        while count>0:
            qinyun_sql = 'select *from products where brand_id=%s and  offline!=1 and gender not in ("male","female")  and region in ("uk","us","cn","it","fr","se","jp") limit  %s,500'%(brand_id,get_sum)
            logging.info(qinyun_sql)
            qingyun_cursor.execute(qinyun_sql)
            results = qingyun_cursor.fetchall()
            #global_result=[]
            #thread=threading.Thread(target=get_result,args=(qinyun_sql,))
            #time.sleep(300)
            count = len(results)
            if count==0:
                sendemail('连接超时'+str(brand_id))
                break
            get_sum += count
            print(qinyun_sql)
            print(count)
            for result in results:
                try:
                    region=result['region']
                    brand_id=result['brand_id']
                    model=result['model']
                    name = result['name']
                    if not name:
                        name = ''
                    else:
                        name=name.replace("'",'"')
                    category=result['category']
                    if not category:
                        category=''
                    else:
                        category=category.replace("'",'"')
                    url=result['url']
                    if not url:
                        url=''
                    color=result['color']
                    if not color:
                        color=''
                    else:
                        color=color.replace("'",'"')
                    spec=result['spec']
                    if not spec:
                        spec=''
                    else:
                        spec=spec.replace("'",'"')
                    description=result['description']
                    if not description:
                        description=''
                    else:
                        description=description.replace("'",'"')
                    details=result['details']
                    if not details:
                        details=''
                    else:
                        details=details.replace("'",'"')
                    gender=result['gender']
                    if not gender:
                        gender='0'
                    price=result['price']
                    if not price:
                        price='0'
                    price_discount=result['price_discount']
                    if not price_discount:
                        price_discount='0'
                    price_change=result['price_change']
                    if not price_change:
                        price_change='0'
                    fetch_time=result['fetch_time']
                    if fetch_time:
                        fetch_time=str(fetch_time)
                    else:
                        fetch_time=''

                    update_time = result['update_time']
                    if update_time:
                        update_time = str(update_time)
                    else:
                        update_time = ''

                    touch_time = result['touch_time']
                    if touch_time:
                        touch_time = str(touch_time)
                    else:
                        touch_time = ''
                    modified=result['modified']
                    if not modified:
                        modified=''
                    update_flag=result['update_flag']
                    if not update_flag:
                        update_flag=''
                    offline=result['offline']
                    if not offline:
                        offline=''
                    fingerprint=result['fingerprint']
                    if not fingerprint:
                        fingerprint=''
                    offline_time=result['offline_time']
                    if not offline_time:
                        offline_time=''
                    model_change=result['model_change']
                    if not model_change:
                        model_change='0'
                    markdel=result['markdel']
                    if not markdel:
                        markdel='0'
                    into_ali_sql1='insert into products(region,brand_id,model,name,category,url,color,spec,description,details,gender,'
                    into_ali_sql2= 'price,price_discount,price_change,fetch_time,update_time,touch_time,offline,offline_time,fingerprint)  VALUES '
                    into_ali_sql3="('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(region,brand_id,model,name,category,url,color,spec,description,details,gender,price,price_discount,price_change,fetch_time,update_time,touch_time,offline,offline_time,fingerprint)
                    into_ali_sql=into_ali_sql1+into_ali_sql2+into_ali_sql3
                    image_true=process_image(fingerprint)
                    print(image_true)
                    if image_true:
                        ali_cursor.execute(into_ali_sql)
                        conn_ali.commit()
                        success_sum+=1
                    print(success_sum)
                except Exception as e:
                    logging.error(str(e)+str(region))
                    print(success_sum)
                    fail_sum += 1
    except Exception as e:
        logging.error(e)
    logging.info('查询出 %s 条数据'%get_sum)
    logging.info('成功导入 %s条数据'%success_sum)
    logging.info('导入失败%s条数据'%fail_sum)
    try:
        if success_sum!=0:
            sendemail(str(brand_id)+'查询出 %s 条数据\n'%get_sum+'成功导入 %s条数据\n'%success_sum+'导入失败%s条数据\n'%fail_sum)
    except Exception as e:
        logging.error(str(e))
    get_sum=0
    success_sum=0
    fail_sum=0
def sendemail(data):
    msg = MIMEText(data, _subtype='html', _charset='utf-8')
    # msg = MIMEMultipart('alternative')
    msg['Subject'] = u'数据迁移到阿里云'
    msg['From'] = 'huagnkaijie <kaijie.huang@mfashion.com.cn>'
    msg['To'] = '2499090390@qq.com'
    server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
    server.login('buddy@mfashion.com.cn', 'rose123')
    server.sendmail('buddy@mfashion.com.cn',['2499090390@qq.com'], msg.as_string())
def process_image(fingerprint):
    global product_image_time
    sql_image='select * from products_image WHERE update_time>"%s" AND  fingerprint="%s"'%(product_image_time,fingerprint)
    product_image_cursor.execute(sql_image)
    result_image=product_image_cursor.fetchall()
    flag_image = False
    count_products_image=0
    print('+++++++++++++++')
    for result in result_image:
        count_products_image+=1
        image_checksum=result['checksum']
        sql_store='select * from images_store where checksum="%s"  and update_time>"%s"'%(image_checksum,product_image_time)
        image_store_cursor.execute(sql_store)
        result_store=image_store_cursor.fetchall()
        count_images_store=0
        for store in result_store:
            count_images_store+=1
            checksum=store['checksum']
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
                    'insert into products_image (idproducts_image,checksum,brand_id,model,fingerprint,update_time,rank) VALUES ("%s","%s","%s","%s","%s","%s","%s")' % (
                    idproducts_image, image_checksum, brand, model, fingerprint, update_time, rank))
                conn_ali.commit()
                conn_ali.commit()
                flag_image=True
            except Exception as e:
                conn_ali.rollback()
                conn_ali.rollback()
                if 'duplicate' in str(e).lower():
                    flag_image=True
                logging.error(str(e))
    return flag_image


def get_update_time():
    brand_list=[
    10166,10178,10184,10192,10212,10220,10226,10239,10248,10259,10263,10264,10268,10270,10300]
    #brand_list=[10049,10066,
    #10308,10316,10322,10333,10350,10354,10367,10369,10373,10385,10388,10429,10510,10669,10856,10897,10946,11301,11614,13084,13902,
    #14022,14097,14162,14163,14997]
    global product_image_time
    for brand_id in brand_list:
        try:
            update_time_sql='SELECT * FROM products_core.images_store where path like "'+str(brand_id)+ "%" '"and update_time>"2016-12-29 07:57:09" order by update_time asc limit 1'
            print(brand_id)
            print(update_time_sql)
            product_image_time=image_store_cursor.execute(update_time_sql)
            result=image_store_cursor.fetchone()
            get_qinyun(brand_id)
            print(result['update_time'])
        except Exception as e:
            print(e)
success_sum=0
fail_sum=0
get_sum=0
product_image_time=''
if __name__=='__main__':
    get_update_time()
    conn_ali.close()
    conn_qinyun.close()
