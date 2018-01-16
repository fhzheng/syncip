#! /usr/bin/python
#-*- coding:utf-8 -*-
import urllib.request
from syncDNSPod import *
import sys, traceback
import log
import conf
import sendmail
import redis

# 从前ip
prev_ip=''
# 现在ip
current_ip=''
# 次级域名
sub_domain=conf.get('sub_domain')

exc_type, exc_value, exc_traceback = sys.exc_info()

# ip键
REDIS_IP = 'ip'
# 状态键
REDIS_STATUS = 'status'

# 本次操作的结果状态
R_STATUS = 1
R_MSG = ''

log.write(message='=====START=====')

r = redis.Redis(host=conf.get('redis.host'), port=conf.get('redis.port'), db=conf.get('redis.db'))
prev_ip = r.get(REDIS_IP)
status = r.get(REDIS_STATUS)
try:
	uri = conf.get('ipget.uri')
	request = urllib.request.Request(uri)
	request.add_header('Access-Token', conf.get('ipget.access_token'))
	response = urllib.request.urlopen(request)
	current_ip = response.read()
	current_ip = current_ip.strip()
	log.write(message='Current ip is '+str(current_ip))
except urllib.request.HTTPError as e:
	R_MSG = str(e)
	traceback.print_exc()
	R_STATUS = -1
except Exception as e:
	R_MSG = str(e)
	traceback.print_exc()
	R_STATUS = -1

if prev_ip != current_ip and R_STATUS == 1:
	r.set(REDIS_IP, current_ip)
	dp = syncDNSPod()
	try:
		dp.modifyRecord(sub_domain, current_ip)
	except Exception as e:
		R_MSG = str(e)
		traceback.print_exc()
		R_STATUS = -2
	sendmail.sendmail(current_ip)
elif prev_ip == current_ip and R_STATUS == 1:
	log.write(message='NOT changed')
	r.set(REDIS_STATUS, R_STATUS)
elif R_STATUS != 1:
	sendmail.sendmail(success=False, msg=R_MSG)
else:
	pass
log.write(message='=====DONE=====')