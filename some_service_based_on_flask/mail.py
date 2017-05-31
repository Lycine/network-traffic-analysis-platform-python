#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr,formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def sendemail(to='noreply@jozif.org', subject_path='default-subject-path-change-me', file_name='default-file-name-change-me'):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "noreply@jozif.org"  # 用户名
    mail_pass = "kmryydqxlgetbibb"  # 口令

    sender = 'noreply@jozif.org'
    # receivers = ['noreply@jozif.org']  # 接收邮件formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))
    receivers = to  # 接收邮件
    print 'send mail to: ',
    print to

    # 创建一个带附件的实例
    message = MIMEMultipart()
    # formataddr((Header("突发事件响应中心", 'utf-8').encode(), mail_user.encode('utf-8') if isinstance(mail_user, unicode) else mail_user))
    nickname = "突发事件响应中心".decode('utf-8')
    nickname = "突发事件响应中心"
    message['From'] = formataddr([nickname, mail_user])

    subject = '突发事件响应报告'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('网络流量数据文件：' + str(file_name) + ' 的检测报告', 'plain', 'utf-8'))

    # 构造附件1，传送附件文件
    att1 = MIMEText(open(subject_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename是邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="report.txt"'
    message.attach(att1)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
