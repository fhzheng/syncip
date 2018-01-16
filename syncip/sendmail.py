#! /usr/bin/python
#-*- coding:utf-8 -*-
import traceback
import smtplib
import log
import conf
def sendmail(ip=None, success=True, msg=None):
	n='sendmail'
	gmail_user = conf.get('mail.host_user')
	gmail_password = conf.get('mail.host_pwd')

	sender = gmail_user
	to = [conf.get('mail.to')]
	subject = 'Your IP address has changed!'
	body = 'Current IP address is '+ str(ip)
	if not success:
		subject = 'Your IP address changed failed!'
		body = body + ', but error is ' + str(msg)
	email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sender, ", ".join(to), subject, body)

	try:
	    server = smtplib.SMTP_SSL(conf.get('mail.server_host'), conf.get('mail.server_port'))
	    server.ehlo()
	    server.login(gmail_user, gmail_password)
	    server.sendmail(sender, to, email_text)
	    server.close()

	    log.write(n,'Email sent!')
	except Exception as e:
	    traceback.print_stack()
	    log.write(n,e)
	    log.write(n,'Something went wrong...')
	else:
		pass
	finally:
		pass
