#! /usr/bin/python
#-*- coding:utf-8 -*-
from datetime import datetime
def write(method='main', message='no message', level='INFO'):
	'''write log'''
	print(datetime.now(), "[%s]" % level, method, ':', message)