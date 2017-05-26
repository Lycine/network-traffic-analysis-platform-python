# -*- coding: utf-8 -*-
import json
import os
import sys
import time
from datetime import datetime
import sys
from optparse import OptionParser

# def doCleansing(fname):
reload(sys)
sys.setdefaultencoding('utf-8')
time_start = time.time();
# print fname
config_path = '/Users/hongyu/PycharmProjects/bistu-internet-analysis/data-mining/blacklist-keyword.json'
try:
    # config_path = sys.argv[1]
    print 'config_path: ' + config_path
except:
    print 'no decalre config_path'
with open(config_path, 'r') as f:
    val = f.read()
    config = json.loads(val)

# origin_blacklist_keyword = config['blacklist-keyword']
# print type(origin_blacklist_keyword)
#
# blacklist_keyword = []
# for b in origin_blacklist_keyword:
#     blacklist_keyword.append(b)
# print origin_blacklist_keyword
blacklist_keyword = config['blacklist-keyword']

print 'read source file...'
# source_file = open("/Users/hongyu/Desktop/2016-08-05-16-new.txt", 'rb')
# source_file = open("/Users/hongyu/Desktop/2016-08-05-05-new-demo.txt", 'rb')
source_file = open(sys.argv[1],'rb')
# print 'fname: ',
# print fname
# source_file = fname
count = 0
count2 = 1
dstipList = []
newf = file("/Users/hongyu/PycharmProjects/bistu-internet-analysis/data-mining/ITEMSET-DATASET.csv", "w+")
# new2f = file("ITEMSET-DATASET.json", "w+")
# new3f = file("Scatter3D.json", "w+")
# new3f.writelines('[')
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
        # print 'len: ' + str(len(mylist))
        mylist = []
        termHostnameCount.sort(key=lambda k: k[1], reverse=True)
        termHostnameCount = termHostnameCount[0:20]
        time_end = time.time()  # time.time()为1970.1.1到当前时间的毫秒数
        result = ''
        for j in termHostnameCount:
            result += str(j[0]) + ','
        if len(termHostnameCount) != 0:
            # print "et: ",
            # print time_end - time_start,
            # print "s startTimeStamp: ",
            # print str(old_timestamp)
            # print "hostnameSize: ",
            # print str(len(termHostnameCount)),
            # print ', ',
            # print str(termHostnameCount)
            d = {}
            d['startTimeStamp'] = str(old_timestamp)
            d['hostnameCount'] = termHostnameCount
            # new2f.writelines(json.dumps(d) + '\n')

            # for item in termHostnameCount:
            #     li = []
            #     li.append(old_timestamp)
            #     li.append(item[0])
            #     li.append(item[1])
            #     new3f.writelines(json.dumps(li) + ',' + '\n')
            newf.writelines(result[:-1] + '\n')  # 去除末尾逗号
        old_timestamp = i['timestamp']
    else:
        mylist.append(str(i['hostname']).split(',')[0].split(':')[0])
newf.close()
# new3f.writelines(']')
# new3f.close()
# print 'len: ' + str(len(hostnameList))
# hostnameSet = set(hostnameList)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
# hostnameCountList = []
# for item in hostnameSet:
#     hostnameCount = ()
#     hostnameCount = (str(item), hostnameList.count(item))
#     hostnameCountList.append(hostnameCount)
# hostnameCountList.sort(key=lambda k: k[1], reverse=True)
# hostnameCountList = hostnameCountList[0:20]
# print "et: ",
# time_end = time.time()  # time.time()为1970.1.1到当前时间的毫秒数
# print time_end - time_start,
# print str(hostnameCountList)
# d = {}
# d['startTimeStamp'] = '0'
# d['hostnameCount'] = hostnameCountList
# new2f.writelines(json.dumps(d) + '\n')
# new2f.close()


# if __name__ == "__main__":
#
#     optparser = OptionParser()
#     optparser.add_option('--inputFile',
#                          dest='input',
#                          help='filename containing csv',
#                          default=None)
#                          # default='ITEMSET-DATASET.csv')
#
#     (options, args) = optparser.parse_args()
#     inFile = None
#     if options.input is None:
#         inFile = sys.stdin
#         print 'wrong'
#     elif options.input is not None:
#         print "options.input",
#         print options.input
#         doCleansing(options.input)
#         print 'success'
#     else:
#         print 'No dataset filename specified, system with exit\n'
#         sys.exit('System will exit')

# python data-mining/data-cleansing.py --inputFile /Users/hongyu/Desktop/2016-08-05-05-new-demo.txt

# python data-mining/data-cleansing.py /Users/hongyu/Desktop/2016-08-05-05-new-demo.txt