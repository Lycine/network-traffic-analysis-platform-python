# -*- coding: utf-8 -*-
import json
import os
import sys
import time
from datetime import datetime
import sys
from optparse import OptionParser

reload(sys)
sys.setdefaultencoding('utf-8')
time_start = time.time()
config_path = '/home/hongyu/PycharmProjects/network-traffic-analysis-platform-python/data-mining/blacklist-keyword.json'
try:
    print 'config_path: ' + config_path
except:
    print 'no decalre config_path'
with open(config_path, 'r') as f:
    val = f.read()
    config = json.loads(val)

blacklist_keyword = config['blacklist-keyword']

print 'read source file...'
# source_file = open("/Users/hongyu/Desktop/2016-08-05-16-new.txt", 'rb')
source_file = open(sys.argv[1],'rb')

count = 0
count2 = 1
dstipList = []
newf = file("/home/hongyu/PycharmProjects/network-traffic-analysis-platform-python/data-mining/ITEMSET-DATASET.csv", "w+")

hostnameAndTimeStampList = []
hostnameList = []
for line in source_file:
    try:
        newLine = line.split(',')
        if str(newLine[7]) == 'HTTP' and str(newLine[6]) == 'HTTP':
            if str(newLine[12]) != '':
                for i, black_keyword in enumerate(blacklist_keyword):
                    if black_keyword not in str(newLine[12]):
                        if i == len(blacklist_keyword) - 1:
                            # 只要时间戳和hostname
                            d = dict()
                            d['hostname'] = str(newLine[12])
                            d['timestamp'] = str(newLine[4])
                            hostnameAndTimeStampList.append(d)
                            hostnameList.append(str(newLine[12]))
                    else:
                        break
    except Exception, e:
        print e
    count += 1
hostnameAndTimeStampList.sort(key=lambda k: (k.get('timestamp', 0)))
old_timestamp = 0
itemset = ''
time_end = time.time()  # time.time()为1970.1.1到当前时间的毫秒数
print time_end - time_start,
print "s"
mylist = []
for i in hostnameAndTimeStampList:
    new_timestamp = i['timestamp']
    termHostnameCount = []

    if (int(new_timestamp) - int(old_timestamp)) > 10:
        myset = set(mylist)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
        for item in myset:
            hostnameCount = ()
            hostnameCount = (str(item), mylist.count(item))
            termHostnameCount.append(hostnameCount)
        mylist = []
        termHostnameCount.sort(key=lambda k: k[1], reverse=True)
        termHostnameCount = termHostnameCount[0:20]
        time_end = time.time()  # time.time()为1970.1.1到当前时间的毫秒数
        result = ''
        for j in termHostnameCount:
            result += str(j[0]) + ','
        if len(termHostnameCount) != 0:
            d = dict()
            d['startTimeStamp'] = str(old_timestamp)
            d['hostnameCount'] = termHostnameCount
            newf.writelines(result[:-1] + '\n')  # 去除末尾逗号
        old_timestamp = i['timestamp']
    else:
        mylist.append(str(i['hostname']).split(',')[0].split(':')[0])
newf.close()