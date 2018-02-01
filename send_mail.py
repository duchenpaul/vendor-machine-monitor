#! /usr/bin/env python3  
# -*- coding: utf-8 -*-   
import sys 
# reload(sys) 
# sys.setdefaultencoding('gb2312')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getopt
from os.path import basename

#Usage: python send_an_email_with_attachment.py subject content (-f FILEPATH -r "RECIPIENT_1@gmail.com,RECIPIENT_2@gmail.com")

SMTP_SERVER = 'smtp.126.com'

fromAddr = "RECIPIENT_1@gmail.com"
# fromAddr = "RASPBERRY_PI<RECIPIENT_1@gmail.com>"
PASSWORD = "Mail_pa55w0rd"

toAddr = "RECIPIENT_1@gmail.com"
#toaddr = "RECIPIENT_1@gmail.com"

def send_mail(subject, content, attach_file = None, recipients = toAddr):
	'''Usage: python send_an_email_with_attachment.py subject content (subject, content, attach_file = <FILEPATH>, recipients = "RECIPIENT_1@gmail.com,RECIPIENT_2@gmail.com")'''
	fromAddr = "RECIPIENT_1@gmail.com"
	toAddr = "RECIPIENT_1@gmail.com"
	msg = MIMEMultipart()
	 
	# msg["Accept-Language"]="zh-CN"
	# msg["Accept-Charset"]="ISO-8859-1,utf-8"

	# msg['Subject'] = sys.argv[1]
	# # body = ''.join(sys.argv[2]).encode('utf-8')
	# body = ''.join(sys.argv[2])

	msg['Subject'] = subject
	body = ''.join(content)
	
	body = body.replace('\n', '<br />')

	if not (attach_file is None):
		filename =  basename(attach_file)
		attachment = open(attach_file, "rb")
		
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		
		msg.attach(part)

	if not (recipients is None):
		toAddr = recipients

	msg.attach(MIMEText('<html><body>'+ body +'</body></html>','html','utf-8'))
	#msg.attach(MIMEText(body, 'plain'))

	msg['From'] = fromAddr
	msg['To'] = toAddr

	print(("sending mail to: %s" % toAddr))

	try: 
		server = smtplib.SMTP(SMTP_SERVER)
		server.starttls()
		server.login(fromAddr, PASSWORD)
		text = msg.as_string()
		#print(text)
		server.sendmail(fromAddr, toAddr.split(','), text)
		server.quit()
		#print("Mail sent")
	except Exception as e:
		print(('Failed to send mail: '+ str(e)))
		sys.exit(1)

if __name__ == '__main__':
	'''Usage: python send_an_email_with_attachment.py subject content (-f FILEPATH -r "RECIPIENT_1@gmail.com,RECIPIENT_2@gmail.com")'''
	subject = sys.argv[1]
	content = sys.argv[2]
	FILE_PATH = None
	toaddr = None

	opts, args = getopt.getopt(sys.argv[3:], "f:r:")
	for op, VALUE in opts:
		if op == '-f':
			FILE_PATH = VALUE
		elif op == '-r':
			toaddr = VALUE

	send_mail(subject, content, FILE_PATH, toaddr)