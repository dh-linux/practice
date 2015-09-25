#!/usr/bin/env  python
# *-*coding:utf-8*-*
import smtplib
import logging
from email.mime.text import MIMEText
from django.conf import settings

# 发送邮件
def send_mail(from_addr,to_addr,sub,content):
    logger = logging.getLogger('django.notify')
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = from_addr
    msg['To'] = to_addr
    
    agent_from = "<" + settings.MAIL_USER + "@autonavi.com>"
    
    try:
        server = smtplib.SMTP()
        server.connect(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(settings.MAIL_USER, settings.MAIL_PASSWORD)
        server.sendmail(agent_from, to_addr, msg.as_string())
        server.quit()
    except Exception, e:
        logger.error(u'邮件发送失败:' + str(e))
        
        
