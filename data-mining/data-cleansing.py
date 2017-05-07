# -*- coding: utf-8 -*-
import json
import os
import sys
import time
from datetime import datetime


def ip_into_int(ip):
    # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
    # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
    return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))


def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c


def is_my_ip(ip):
    edu_net_ip_list = ['222.249.130.141', '222.249.250.138', '222.249.130.198', '222.249.130.212', '222.249.250.31', '59.64.79.102', '59.64.79.139', '59.64.79.157', '222.249.251.150',
                       '222.249.251.4', '222.249.250.45', '59.64.79.152', '222.249.251.85', '222.249.130.207', '59.64.79.158', '222.249.130.132', '222.249.251.84', '222.249.130.153',
                       '222.249.251.132', '222.249.251.68']
    s = set(edu_net_ip_list)
    return ip in s


source_file = open("/toshibaVolume/BISTU-NETWORK-DATA/2016-08-07-new/2016-08-07-23-new.txt", 'rb')
count = 0
count2 = 1
dstipList = []
newf = file("first-cleansing.txt", "w+")
old_timestamp = 0
itemset = ''
for line in source_file:
    # if count < 1000000:

    try:
        newLine = line.split(',')

        new_timestamp = str(newLine[4])
        print 'new:' + str(new_timestamp)
        print 'old:' + str(old_timestamp)
        if (int(new_timestamp) - int(old_timestamp)) > 10:
            print itemset
            newf.writelines(itemset)
            itemset = ''
            old_timestamp = str(newLine[4])
            #  if is_my_ip(str(newLine[0])):
        if str(newLine[7]) == 'HTTP' and str(newLine[6]) == 'HTTP':
            if str(newLine[12]) != '':
                # dstipList.append(newLine[0])
                # print count2, str(line[0]),  str(line[12])
                # print line
                # str(line[6]), str(line[7]), str(line[8]), str(line[9]),

                # cleansed_line = str(newLine[12])+','+str(newLine[4]) + ','

                itemset += str(newLine[12]) + ','
#                print itemset
                #newf.writelines(cleansed_line)
                # count2 += 1
    except Exception, e:
        print e
    count += 1
    # else:
    #     break
newf.close()
dstipSet = set(dstipList)
print dstipSet
# 内网ip->HTTP->
