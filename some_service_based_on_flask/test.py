#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path

from some_service_based_on_flask.mail import sendemail

rootdir = "/Users/hongyu/PycharmProjects/bistu-internet-analysis/some_service_based_on_flask/"  # 指明被遍历的文件夹
result = []

for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for dirname in dirnames:  # 输出文件夹信息
        print "parent is:" + parent
        print "dirname is" + dirname
    for i, filename in enumerate(filenames):  # 输出文件信息
        print "parent is:" + parent
        print "**filename is:" + filename
        print "**the full name of the file is:" + os.path.join(parent, filename)  # 输出文件路径信息
        result.append([i, filename, os.path.join(parent, filename)])
print result

sendemail(to='513736920@qq.com', subject_path='test.py',
          file_name='subject')