# -*- coding: utf-8 -*-
import math
import os
import smtplib
import subprocess
import sys
import time
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from elasticsearch import Elasticsearch
from elasticsearch import helpers

ROOT_DIR = "/toshibaVolume/BISTU-NETWORK-DATA/target"
ES_INDEX = "bistu-internet-data-"
ES_TYPE = "network-metadata"
ES_USERNAME = "elastic"
ES_PASSWORD = "changeme"
ES_HOSTNAME = "localhost"
ES_PORT = "9200"
is_mute = True

MAIL_PASS = ""
MAIL_SUBJECT = ""
MAIL_CONTENT = ""
MAIL_FROM_NAME = ""
MAIL_TO_NAME = ""
MAIL_FROM_ADDR = ""
MAIL_TO_ADDR = ""
MAIL_SMTP = ""


def speak(message="nothing", is_mute=True):
    if is_mute:
        pass
    else:
        command = 'espeak -ven+f3 -k5 -s150 --punct="<characters>" "%s" 2>>/dev/null' % message
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        return output


def convert_time(seconds):
    day = 24 * 60 * 60
    hour = 60 * 60
    minutes = 60
    if seconds < 60:
        return "%ds" % math.ceil(seconds)
    elif seconds > day:
        days = divmod(seconds, day)
        return "%dd,%s" % (int(days[0]), convert_time(days[1]))
    elif seconds > hour:
        hours = divmod(seconds, hour)
        return '%dh,%s' % (int(hours[0]), convert_time(hours[1]))
    else:
        minutess = divmod(seconds, minutes)
        return "%dm,%ds" % (int(minutess[0]), math.ceil(minutess[1]))


def show_status():
    end = time.clock()
    print(
        'used time: %s' % convert_time((end - START_TIME)) +
        ', errorCount: ' + str(errorCount) +
        ', speed: ' + str(round(count / (end - START_TIME), 2)) + 'rows/sec' +
        ', count/total: ' + str(count) + '/' + str(total) +
        ', remain time: ' + convert_time(round((total - count) / (count / (end - START_TIME)), 0)) +
        ', finish: ' + str(round((count + 0.0) / total * 100, 2)) + '%'),


def send_email(content=MAIL_CONTENT,
               subject=MAIL_SUBJECT,
               from_name=MAIL_FROM_NAME,
               to_name=MAIL_TO_NAME,
               from_addr=MAIL_FROM_ADDR,
               to_addr=MAIL_TO_ADDR,
               mail_password=MAIL_PASS,
               smtp_server=MAIL_SMTP):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = _format_addr(from_name + u' <%s>' % from_addr)
    msg['To'] = _format_addr(to_name + u' <%s>' % to_addr)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(from_addr, mail_password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


mapping = '''
{
    "settings": {
        "number_of_shards": 20
    },
    "mappings": {
        "client": {

            "properties": {
                "source_ip": {
                        "type": "ip"
                    },
                    "destination_ip": {
                        "type": "ip"
                    },
                    "sourceTransportPort": {
                        "type": "string"
                    },
                    "destinationTransportPort": {
                        "type": "string"
                    },
                    "flowStartSeconds": {
                        "type": "date"
                    },
                    "flowEndSecond": {
                        "type": "date"
                    },
                    "applicationProtocolName": {
                        "type": "string"
                    },
                    "applicationName": {
                        "type": "string"
                    },
                    "applicationCategoryName": {
                        "type": "string"
                    },
                    "applicationSubCategoryName": {
                        "type": "string"
                    },
                    "http_method": {
                        "type": "string"
                    },
                    "status": {
                        "type": "string"
                    },
                    "http_hostname": {
                        "type": "string"
                    },
                    "http_referer": {
                        "type": "string"
                    },
                    "httpRequestLabelNum": {
                        "type": "integer"
                    },
                    "httpReplyLabelNum": {
                        "type": "integer"
                    },
                    "httpRequestVersion": {
                        "type": "string"
                    },
                    "httpReplyVersion": {
                        "type": "string"
                    },
                    "fileName": {
                        "type": "string"
                    },
                    "fileEncrypt": {
                        "type": "string"
                    },
                    "fileType": {
                        "type": "string"
                    },
                    "fileSize": {
                        "type": "float"
                    },
                    "fileMd5": {
                        "type": "string"
                    },
                    "DNSReplyCode": {
                        "type": "integer"
                    },
                    "DNSQueryName": {
                        "type": "string"
                    },
                    "DNSDelay": {
                        "type": "float"
                    },
                    "DNSReplyIPv4": {
                        "type": "string"
                    },
                    "SrcArea": {
                        "type": "string"
                    },
                    "DestArea": {
                        "type": "string"
                    },
                    "SrcIPUser": {
                        "type": "string"
                    },
                    "DestIPUser": {
                        "type": "string"
                    },
                    "SrcGeographyLocationCountryOrRegion": {
                        "type": "string"
                    },
                    "SrcGeographyLocationCity": {
                        "type": "string"
                    },
                    "SrctGeographyLocationLatitudeLongitude": {
                        "type": "geo_point"
                    },
                    "DestGeographyLocationCountryOrRegion": {
                        "type": "string"
                    },
                    "DestGeographyLocationCity": {
                        "type": "string"
                    },
                    "DestGeographyLocationLatitudeLongitude": {
                        "type": "geo_point"
                    }
            }
        }
    }
}
'''
speak("launch script", is_mute)
reload(sys)
sys.setdefaultencoding('utf8')
actions = []
errorCount = 0
es = Elasticsearch(
    [
        'http://' + ES_USERNAME + ':' + ES_PASSWORD + '@' + ES_HOSTNAME + ':' + ES_PORT + '/'
    ],
    verify_certs=True
)

for parent, dir_names, file_names in os.walk(ROOT_DIR):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for filename in file_names:  # 输出文件信息
        new_filename = filename.split("-")[0:4]
        index_suffix = ""
        for part in new_filename:
            index_suffix += part
        temp_index = ES_INDEX + index_suffix
        print "index: " + temp_index
        es.indices.create(index=temp_index, ignore=400, body=mapping)
        START_TIME = time.clock()
        count = 0
        speak("new task begin", is_mute)
        print "running file:" + os.path.join(parent, filename)  # 输出文件路径信息
        lines = open(os.path.join(parent, filename), 'rb').readlines()
        total = len(lines)
        print "total rows: " + str(total)
        source_file = open(os.path.join(parent, filename), 'rb')
        for line in source_file:
            try:
                line = line.split(',')
                action = {
                    "_index": temp_index,
                    "_type": ES_TYPE,
                    "_source": {
                        "source_ip": line[0],
                        "destination_ip": line[1],
                        "sourceTransportPort": str(line[2]),
                        "destinationTransportPort": str(line[3]),
                        "flowStartSeconds": datetime.fromtimestamp(int(line[4]) + 0.0),
                        "flowEndSecond": datetime.fromtimestamp(int(line[5]) + 0.0),
                        "applicationProtocolName": str(line[6]),
                        "applicationName": str(line[7]),
                        "applicationCategoryName": str(line[8]),
                        "applicationSubCategoryName": str(line[9]),
                        "http_method": str(line[10]),
                        "status": str(line[11]),
                        "http_hostname": str(line[12]),
                        "http_referer": str(line[13]),
                        "httpRequestLabelNum": line[14],
                        "httpReplyLabelNum": str(line[15]),
                        "httpRequestVersion": str(line[16]),
                        "httpReplyVersion": str(line[17]),
                        "fileName": str(line[18]),
                        "fileEncrypt": str(line[19]),
                        "fileType": str(line[20]),
                        "fileSize": str(line[21]),
                        "fileMd5": str(line[22]),
                        "DNSReplyCode": line[23],
                        "DNSQueryName": str(line[24]),
                        "DNSDelay": str(line[25]),
                        "DNSReplyIPv4": str(line[26]),
                        "SrcArea": str(line[28]),
                        "DestArea": str(line[29]),
                        "SrcIPUser": str(line[30]),
                        "DestIPUser": str(line[31]),
                        "SrcGeographyLocationCountryOrRegion": str(line[32]),
                        "SrcGeographyLocationCity": str(line[33]),
                        "SrcGeographyLocationLatitudeLongitude": str(line[35]) + ", " + str(line[34]),
                        "DestGeographyLocationCountryOrRegion": str(line[36]),
                        "DestGeographyLocationCity": str(line[37]),
                        "DestGeographyLocationLatitudeLongitude": str(line[39]) + ", " + str(line[38])
                    }
                }
                count += 1
                actions.append(action)
            except Exception, e:
                print e
            if len(actions) == 24000:
                try:
                    for ok, info in helpers.parallel_bulk(es, actions=actions, thread_count=8, chunk_size=40000,
                                                          max_chunk_bytes=8 * 100 * 100 * 1024):
                        if not ok:
                            print('A document failed:', info)
                except Exception, e:
                    print e
                    errorCount += 1
                del actions[0:len(actions)]
                print '\r',
                show_status()

        if len(actions) > 0:
            for ok, info in helpers.parallel_bulk(es, actions=actions, thread_count=8, chunk_size=40000,
                                                  max_chunk_bytes=8 * 100 * 100 * 1024):
                if not ok:
                    print('A document failed:', info)
            del actions[0:len(actions)]
            source_file.close()
            show_status()
        source_file.close()
        speak("task complete", is_mute)
        content = filename + " <br>complete!"
        send_email(content)
        print " "
        print " "
        time.sleep(1)
speak("all task complete", is_mute)
send_email("all task complete")
