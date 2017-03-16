# coding:utf8
import math
import os
import smtplib
import subprocess
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

MAIL_PASS = ""
MAIL_SUBJECT = ""
MAIL_CONTENT = ""
MAIL_FROM_NAME = ""
MAIL_TO_NAME = ""
MAIL_FROM_ADDR = ""
MAIL_TO_ADDR = ""
MAIL_SMTP = ""
PENDING_DIR = ""
FINISH_DIR = ""


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


def extract_index_suffix(filename):
    filename = "2016-08-08-00-new.txt"
    filename = filename.split("-")[0:4]
    index_suffix = ""
    for part in filename:
        index_suffix += part
    return index_suffix


def speak(message):
    command = 'espeak -ven+f3 -k5 -s150 --punct="<characters>" "%s" 2>>/dev/null' % message
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output


def traversal_dir(PENDING_DIR):
    for parent, dirnames, filenames in os.walk(PENDING_DIR):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            # print "parent is: " + parent
            # print "filename is: " + filename
            print "the full name of the file is:" + os.path.join(parent, filename)  # 输出文件路径信息


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


def check_pending_task(pending_dir=PENDING_DIR):
    command = "ls -l " + pending_dir + "|tail -n 1 |awk '{print $9}'"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    command2 = " ls -l " + pending_dir + " |wc -l"
    p = subprocess.Popen(command2, stdout=subprocess.PIPE, shell=True)
    (output2, err2) = p.communicate()
    output2 = output2.replace(' ', '')
    print 'reamin task: ' + output2,
    if output == "":
        print "no more pending task"
    return output


def mv_pending2finish(finish_dir=FINISH_DIR, filename="FILENAME"):
    command = "mv " + filename + " " + finish_dir
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    if p.returncode == 0:
        print "move task success"
    else:
        print "move task failure"
        # if output == "":
        #     print "no more pending task"
        # return output


if __name__ == "__main__":
    # send_email()
    print convert_time(123)
    # print extract_index_suffix("2016-08-08-00-new.txt")
    # print traversal_dir("/home/hongyu/Desktop/Bistu_internet_data")
    # speak("aa")

    # next_task = check_pending_task(pending_dir="/Users/hongyu/Desktop/temp/pending_task")
    # if next_task != "":
    #     print "continue"
    # else:
    #     print "nomore"


    # print time.strftime('%H:%M:%S', time.localtime(time.time()))
