#encoding=utf8
import sys
from queue import Queue
print(sys.getdefaultencoding())
import csv
from zipfile import ZipFile
import requests,urllib
import threading,time
from datetime import timedelta
start=time.time()
def downLoader():
    try:
        while True:
            try:
                url=global_queue.get(timeout=5)
                print(url+str(threading.current_thread().name))
            except:
                pass
            try:
                f = requests.get(url, timeout=2)

                with open('file/' + path + '.html', 'w', encoding='utf-8') as ff:
                    ff.write(f.content.decode('utf-8'))
            except:
                pass
        print('end  '+str(threading.current_thread().name))
    except Exception as e:
        print(e)
    pass
global_queue=Queue()
count=1
threads=[]
no=20
for i in range(no):
    threads.append(threading.Thread(target=downLoader))
for i in range(no):
    threads[i].start()

for num,url in csv.reader(open('top-1m.csv')):
    #f=urllib.request.urlopen('http://www.jb51.net/article/70136.htm')
    path=url
    url='http://www.'+url
    global_queue.put(url)
    count+=1
    if count>1000:
        break
print('main end')
for i in range(no):
    threads[i].join()
end=time.time()
print(end-start)
print(timedelta(seconds=(end-start)))