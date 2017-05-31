#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import os.path
import re
import subprocess
import traceback

from flask import Flask
from flask import request, Response
from flask_cors import *

from mail import sendemail

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/', methods=['GET', 'POST'])
def index():  # print 'file_path: ',
    # print file_path
    # print 'emails: ',
    # print emails
    # 只接受post请求
    if request.method == 'POST':
        d = dict()
        d['status'] = 'failed'
        file_path = request.form['file_path']
        emails = request.form['emails']
        # 数据文件参数传过来为空
        if not file_path:
            d['content'] = 'Target file Path Empty!'
            return Response(json.dumps(d), mimetype='application/json;charset=UTF-8')
        # 邮件发送数组参数传过来为空
        if not emails:
            d['content'] = 'Emails Empty!'
            return Response(json.dumps(d), mimetype='application/json;charset=UTF-8')
        print 'file_path: ',
        print file_path
        print 'emails: ',
        print emails
        try:
            emails_list = str(emails).split(';')
            # print emails_list
            for email in emails_list:
                # 检查邮箱格式
                if re.match(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z_]{0,19}.[0-9a-zA-Z_]{0,19}', email):
                    pass
                else:
                    d['content'] = 'Email regex failure!'
                    return Response(json.dumps(d), mimetype='application/json;charset=UTF-8')
        except:
            traceback.print_exc()
            d['content'] = 'Email list error!'
            return Response(json.dumps(d), mimetype='application/json;charset=UTF-8')
        result = ''
        try:
            # "/home/hongyu/PycharmProjects/bistu-internet-analysis-latest/data-mining/apriori-result.txt"
            # 准备工作都已经完成，开始计算
            print 'data_cleansing start'
            data_cleansing(file_path)
            print 'data_cleansing finish'
            print 'apriori start'
            apriori()
            print 'apriori finish'
            apriori_result_directory = '/home/hongyu/PycharmProjects/bistu-internet-analysis-latest/data-mining/'
            apriori_result_file_name = 'result.txt'
            f = open(apriori_result_directory + apriori_result_file_name)  # 返回一个文件对象
            line = f.readline()  # 调用文件的 readline()方法
            while line:
                # print line, item: ('cc.xtgreat.com', 'cm.fastapi.net', 's.haiyunx.com', 's.x.cn.xtgreat.com', 'changyan.sohu.com') ,support: 0.154 # 后面跟 ',' 将忽略换行符
                line = f.readline()
                result += line
                result += '<br/>'
            f.close()
            sendemail(to=emails_list, subject_path=apriori_result_directory + apriori_result_file_name,
                      file_name=str(file_path).split('/', -1)[-1])
        except:
            traceback.print_exc()
            d['content'] = 'Read file failure!'
            return Response(json.dumps(d), mimetype='application/json;charset=UTF-8')
        if result:
            d = dict()
            d['status'] = 'success'
            d['content'] = result
            return Response(json.dumps(d), mimetype='application/json;charset=UTF-8')
        else:
            print 'result',
            print result
            d['content'] = 'Unknown error!'
            return Response(json.dumps(d), mimetype='application/json;charset=UTF-8')
    # 只接受post请求，驳回get请求
    else:
        d = dict()
        d['status'] = 'failed'
        d['content'] = 'Post requests only!'
        return Response(json.dumps(d), mimetype='application/json;charset=UTF-8')


# 以json格式返回可选择的网络流量数据
@app.route('/selectable-files', methods=['GET'])
def request_files():
    rootdir = "/toshibaVolume/BISTU-NETWORK-DATA/finished"  # 指明被遍历的文件夹
    result = []
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        # for dirname in dirnames:  # 输出文件夹信息
        # print "parent is:" + parent
        # print "dirname is" + dirname
        for filename in filenames:  # 输出文件信息
            # print "parent is:" + parent
            # print "**filename is:" + filename
            # print "**the full name of the file is:" + os.path.join(parent, filename)  # 输出文件路径信息
            if not filename.startswith('.'):
                result.append([filename, os.path.join(parent, filename)])
    print 'json:',
    print json.dumps(result)
    return Response(json.dumps(result), mimetype='application/json;charset=UTF-8')


# 同步调用数据清洗
def data_cleansing(fname):
    subprocess.call(
        ["python", "/home/hongyu/PycharmProjects/bistu-internet-analysis-latest/data-mining/data-cleansing.py", fname])


# 同步调用Apriori算法
def apriori():
    subprocess.call(
        ["python", "/home/hongyu/PycharmProjects/bistu-internet-analysis-latest/data-mining/apriori.py", "-f",
         "/home/hongyu/PycharmProjects/bistu-internet-analysis-latest/data-mining/ITEMSET-DATASET.csv"])


if __name__ == "__main__":
    app.run()
