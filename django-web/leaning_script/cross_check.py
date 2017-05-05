# -*- coding:utf-8 -*-
import random
def bucket(filename,bucketName,separator,classColumn):
    data={}
    bucket_numbers=10
    with open(filename) as f:
        lines=f.readlines()
    for line in lines:
        category=line.split()[0]
        data.setdefault(category,[])
        data[category].append(line)

    buckets=[]
    for i in range(bucket_numbers):
        buckets.append([])
    for k in data.keys():
        random.shuffle(data[k])
        bnum=0
        for item in data[k]:
            buckets[bnum].append(item)
            bnum=(bnum+1)%bucket_numbers
    for bnum in range(bucket_numbers):
        with open('%s-%02i'%(bucketName,bnum+1),'w') as f:
            for item in buckets[bnum]:
                f.write(item)
bucket('mpgData.txt','mpgdata','',0)
