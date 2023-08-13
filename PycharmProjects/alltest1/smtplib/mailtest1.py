# 发邮件，发不出去，应该要整cookie
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = '99gelanjingling@gmail.com'
receivers = ['1363180320@qq.com']

message = MIMEText('Python 邮件发送', 'plain', 'utf-8')
message['From'] = Header('yourMom', 'utf-8')
message['To'] = Header('king', 'utf-8')

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("succeed")
except smtplib.SMTPException:
    print("wrong")
