#! /usr/bin/python
#-*- coding:utf-8 -*-
import urllib2
from syncDNSPod import *
import log
import conf
import sendmail

prev_ip=''
current_ip=''
sub_domain=conf.get('sub_domain')

log.write(message='=====START=====')

try:
	with open('ip.txt','r') as f:
		prev_ip=f.read()
        uri = conf.get('ipget.uri')
        request = urllib2.Request(uri)
        request.add_header('Access-Token',conf.get('ipget.access_token'))
        response = urllib2.urlopen(request)
        current_ip = response.read()
        current_ip = current_ip.strip()
	log.write(message='Current ip is '+current_ip)
	if prev_ip!=current_ip:
		f=open(conf.get('file.record_file'),'w')
		f.write(current_ip)
		f.close()
		sendmail.sendmail(current_ip)
		dp=syncDNSPod()
		dp.modifyRecord(sub_domain,current_ip)
	else:
		log.write(message='NOT changed')
	pass
except Exception as e:
	log.write(message=e,level='ERROR')
	raise
	exit()
else:
	pass
finally:
	log.write(message='=====DONE=====')
	pass
