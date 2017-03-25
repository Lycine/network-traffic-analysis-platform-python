# -*- coding: utf-8 -*-
import math
import smtplib
import subprocess
import sys
import time
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

FINISHED_DIR = "/toshibaVolume/BISTU-NETWORK-DATA/finished/"
PENDING_DIR = "/toshibaVolume/BISTU-NETWORK-DATA/pending/"

MAIL_PASS = "kmryydqxlgetbibb"
MAIL_SUBJECT = "csv2es status report"
MAIL_CONTENT = ""
MAIL_FROM_NAME = "Report Robot"
MAIL_TO_NAME = "Administrator of elasticsearch"
MAIL_FROM_ADDR = "513736920@qq.com"
MAIL_TO_ADDR = "513736920@qq.com"
MAIL_SMTP = "smtp.qq.com"

def speak(message="nothing", IS_MUTE=True):
    if IS_MUTE:
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
        return "%d:%s" % (int(days[0]), convert_time(days[1]))
    elif seconds > hour:
        hours = divmod(seconds, hour)
        return '%d:%s' % (int(hours[0]), convert_time(hours[1]))
    else:
        minutess = divmod(seconds, minutes)
        return "%d:%d" % (int(minutess[0]), math.ceil(minutess[1]))

def send_email(content=MAIL_CONTENT,
               subject=MAIL_SUBJECT,
               from_name=MAIL_FROM_NAME,
               to_name=MAIL_TO_NAME,
               from_addr=MAIL_FROM_ADDR,
               to_addr=MAIL_TO_ADDR,
               mail_password=MAIL_PASS,
               smtp_server=MAIL_SMTP):


    try:
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr(
                (Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))


        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = _format_addr(from_name + u' <%s>' % from_addr)
        msg['To'] = _format_addr(to_name + u' <%s>' % to_addr)
        msg['Subject'] = Header(subject, 'utf-8').encode()

        server = smtplib.SMTP(smtp_server, 25)
        server.login(from_addr, mail_password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except:
        pass

def mv_pending2finished(finished_dir=FINISHED_DIR, filename="FILENAME"):
    command = "mv " + filename + " " + finished_dir
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    if p.returncode == 0:
        print "Move task success!"
    else:
        print "Move task failure!"

def check_pending_task(pending_dir=PENDING_DIR):
    command = "ls -l " + pending_dir + "|tail -n 1 |awk '{print $9}'"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    command2 = " ls -l " + pending_dir + " |wc -l"
    p = subprocess.Popen(command2, stdout=subprocess.PIPE, shell=True)
    (output2, err2) = p.communicate()
    output2 = output2.replace(' ', '')
    print 'Remain task: ' + str(int(output2) - 1)
    global REMAIN_TASK
    REMAIN_TASK = str(int(output2) - 1)
    if REMAIN_TASK == 0:
        print "No more pending task."
    return output

mapping = '''
{
    "settings" : {
        "number_of_shards" : 1,
        "number_of_replicas":0
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