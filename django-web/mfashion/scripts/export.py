#coding=utf-8

import datetime,time
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.insert(0,os.path.dirname(os.getcwd()))
import MySQLdb
import json
import requests
import logging
reload(logging)
__author__='黄开杰'

limit_count = 5000
one_send=300
database={}
database['port']=3306
#database['host']='rm-2zeabe2a02n34m358o.mysql.rds.aliyuncs.com'
database['host']='rm-bp1355nz2epe0yon9o.mysql.rds.aliyuncs.com'
database['username']='spider'
database['password']='Be0jx1KRmK'
#database={}#把这个注释掉连接的就是上面配置的这个数据库,如果不注释，连接的就是数据库里面配置的数据库
db_lookbook=database
dbname='lookbook'
db_sku=MySQLdb.connect(host=db_lookbook['host'],port=db_lookbook['port'],user=db_lookbook['username'],passwd=db_lookbook['password'],db=dbname,charset='utf8')#connect to product_sku
db_info=MySQLdb.connect(host=db_lookbook['host'],port=db_lookbook['port'],user=db_lookbook['username'],passwd=db_lookbook['password'],db=dbname,charset='utf8')#connect to product_info
info_cursor=db_info.cursor(cursorclass=MySQLdb.cursors.DictCursor)
sku_cursor=db_sku.cursor(cursorclass=MySQLdb.cursors.DictCursor)
updatetime=datetime.datetime.utcfromtimestamp(time.time()-(24*3600*30))
def processInfo(handl_brand):
    queryInfo = "select * from product_info where (name_cn!=''  or name_en!='')   and  status=1 and update_time >'%s' and  cover_image !='' and  brand_id=%s  limit  %s" % (updatetime,handl_brand,limit_count)
    print (queryInfo)
    info_cursor.execute(queryInfo)
    results = info_cursor.fetchall()
    results_len=len(results)
    global export_sum
    export_sum=results_len
    print ('查询出来的数据条数', results_len)
    total=0
    count_temp=results_len
    global flag
    while  count_temp>0:
        global export_info_sum
        data = []
        print ('开始打包数据')
        for result in results[total:(total+one_send)]:
            export_info_sum+=1
            spu_id = str(result['spu_id'])
            brand_id = result['brand_id']
            brand_name_cn = result['brand_name_cn']
            brand_name_en = result['brand_name_en']
            offline_time=result['offline_time']
            price_history=result['price_history']
            name_cn = result['name_cn']
            if  not name_cn:
                name_cn=''
            name_en = result['name_en']
            if not name_en:
                name_en=''
            description_cn = result['description_cn']
            if not description_cn:
                description_cn=''

            description_en = result['description_en']
            if not description_en:
                description_en=''
            model = result['model']
            details_cn = result['details_cn']

            details_en = result['details_en']
            if not details_en:
                details_en=''
            if not details_cn:
                details_cn=''
            category_first = result['category_first']
            category_last = result['category_last']
            gender = result['gender']
            price = result['price']
            price_discount = result['price_discount']
            if not price_discount:
                price_discount=0
            region = result['region']
            currency = result['currency']
            tag_list = result['tag_list']
            if not tag_list:
                tag_list=''
            cover_image = result['cover_image']
            opt_cover_image = result['opt_cover_image']
            if not opt_cover_image:
                opt_cover_image=''
            image_list = result['image_list']
            fetch_time = result['fetch_time']
            touch_time = result['touch_time']
            offline = result['offline']
            status = result['status']
            url_list = result['url_list']
            attrs = result['attrs']
            if not attrs:
                attrs=''
            sku_list=getSku(spu_id)
            if not sku_list:
                continue
                sku_list=[]
            data_temp={}
            data_temp['spu_id']=spu_id
            data_temp['brand_id']=int(brand_id)
            data_temp['brand_name_cn']=brand_name_cn
            data_temp['brand_name_en'] = brand_name_en
            data_temp['name_cn']=name_cn
            data_temp['name_en']=name_en
            data_temp['description_cn']=description_cn
            data_temp['description_en'] = description_en
            data_temp['model']=model
            data_temp['details_cn']=details_cn
            data_temp['details_en']=details_en
            data_temp['category_first']=category_first
            data_temp['category_last']=category_last
            data_temp['gender']=gender
            data_temp['price']=price
            data_temp['price_discount']=price_discount
            data_temp['region']=region
            data_temp['currency']=currency
            data_temp['tag_list']=tag_list
            data_temp['cover_image']=cover_image

            data_temp['opt_cover_image']=opt_cover_image
            data_temp['image_list']=image_list
            data_temp['fetch_time']=str(fetch_time)
            data_temp['touch_time']=str(touch_time)
            data_temp['offline']=offline
            if offline_time:
                data_temp['offline_time']=str(offline_time)
            if price_history:
                data_temp['price_history']=price_history
            data_temp['status']=status
            data_temp['url_list']=url_list
            data_temp['attrs']=attrs
            data_temp['sku_list']=sku_list
            data.append(data_temp)
        #url1 = 'https://tmoses.ofashion.com.cn:8014/sync_product_info'#测试接口look
        #url2 = 'https://tmoses.ofashion.com.cn:8012/sync_product_info'  # 测试接口mfashion
        #url4='http://123.59.12.73/sync_product_info'#线上mfashion

        print ('开始发送  本次发送的数据量为 ', len(data))
        print ('当前处理品牌为 ', handl_brand)
        print ('数据发往lookbook库')
        #url = 'https://lookbookapi.ofashion.com.cn/sync_product_info?no_check=1'  # 线上loobook
        url = 'https://tmoses.ofashion.com.cn:8014/sync_product_info'  # 测试接口look
        sendPost3(url, data)
    #elif flag=="mfashion":
        print ('开始发送  本次发送的数据量为 ', len(data))
        print ('当前处理品牌为 ', handl_brand)
        print ('数据发往ofashion库')
        #url = 'http://123.59.12.73/sync_product_info?no_check=1' #线上mfashion
        url = 'https://tmoses.ofashion.com.cn:8012/sync_product_info'  # 测试接口mfashion
        sendPost3(url, data)
        total+=one_send
        count_temp-=one_send
    export_info_sum = 0
    export_sku_sum = 0
    export_sum = 0


    #sendPost2('https://tmoses.ofashion.com.cn:8012/internal_service/sync_product_info',date)

def sendPost3(url,data):
    try:
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, data=json.dumps(data), headers=headers,verify=False);
        get_data=json.loads(r.text)
        print (get_data["original"]["msg"],'\n')
    except Exception as ex:
        print (ex)




def getSku(spu_id):
    sku_list=[]
    sku_cursor.execute("select * from product_sku where status=1 and price!=0 and  spu_id='%s'"%spu_id)
    #print "select * from product_sku where status=1 and  spu_id='%s'"%spu_id
    results=sku_cursor.fetchall()
    global export_sku_sum
    export_sku_sum+=len(results)
    for result in results:
        spec=result['spec']
        color=result['color']
        region=result['region']
        currency=result['currency']
        price=result['price']
        price_discount=result['price_discount']
        status=result['status']
        sku_list_temp={}
        sku_list_temp['spu_id']=spu_id
        sku_list_temp['color']=color
        sku_list_temp['region']=region
        sku_list_temp['currency']=currency
        sku_list_temp['price']=price
        sku_list_temp['price_discount']=price_discount
        sku_list_temp['status']=status
        sku_list_temp['spec']=spec
        sku_list.append(sku_list_temp)
    return sku_list
export_info_sum=0
export_sku_sum=0
export_sum=0
flag=0
if __name__=='__main__':
    brand_list=[]
    try:
        brand_list.append(sys.argv[1])
        #logging.basicConfig(level=logging.INFO,format='[line: %(lineno)d]  [time:%(asctime)s]  %(levelname)s :  %(message)s',datefmt='%Y-%m-%d %H:%M',filename='/data/data_group/storage/log/'+'%srelease.log'%handle_brand_id,filemode='w')
        pass
    except Exception as e:
        print (e)
    else:

        try:
            #brand_list = [10066,10376,10697,10259,10066,10388]

            for handle_brand_id in brand_list:
                print (handle_brand_id)
                print ('开始处理')
                processInfo(handle_brand_id)
                #print '本次共更新'+str(update_sum), '本次共插入'+str(insert_sum)
        except Exception as e:
            print (e)
    db_info.close()
    info_cursor.close()




