#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


def sendemail(to='noreply@jozif.org', subject_path='default-subject-path-change-me', file_name='default-file-name-change-me'):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "noreply@jozif.org"  # 用户名
    mail_pass = "kmryydqxlgetbibb"  # 口令

    sender = 'noreply@jozif.org'
    # receivers = ['513736920@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    receivers = to  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 创建一个带附件的实例
    message = MIMEMultipart()

    # message['From'] = Header("突发事件响应中心", 'utf-8')
    message['From'] = formataddr(["突发事件响应中心", mail_user])

    subject = '突发事件响应报告'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('网络流量数据文件：' + str(file_name) + ' 的检测报告', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(subject_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="test.txt"'
    message.attach(att1)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
