"""
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from lib import com_config, com_logger


def send_mail_gmail(subject, table, filename = ''):
    conf = com_config.Config()
    config = conf.getconfig()
    logger = com_logger.Logger('Email')
    logger.info('Sending email')
    msg = MIMEMultipart()
    
    body = "".join(str(l) for l in table)
    body = body.replace("', '","").replace("['","").replace("']","").replace("', \"","").replace("\" ,'","")

    msg['From'] = config['EMAIL']['from']
    msg['To'] = config['EMAIL']['to']
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    try:
        if len(filename) > 0:
            attachment = open("./" + filename, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)
        
        logger.debug('Try to connect SMTP')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        logger.debug('Connected to SMTP')
        server.starttls()
        logger.debug('Try to connect mail box')
        server.login(config['EMAIL']['from'], config['EMAIL']['password'])
        text = msg.as_string()
        logger.debug('Connected to mailbox')
        logger.debug('Try to send mail')
        server.sendmail(config['EMAIL']['from'], config['EMAIL']['to'], text)
        logger.debug('Mail sent')
        server.quit()
    except Exception as exp:
        logger.critical('Error sending mail')
