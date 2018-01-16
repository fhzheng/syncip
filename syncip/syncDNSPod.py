#! /usr/bin/python
#-*- coding:utf-8 -*-

# import httplib
from urllib import request, parse
import json
from datetime import datetime
import log
import conf

class syncDNSPod:
    '''operate DNSPod
        #dp:short for DNSPod
    '''
    def __init__(self):
        self.__dp_token = conf.get('dnspod.dp_token')
        self.__dp_base = conf.get('dnspod.dp_base')
        self.__dp_name = conf.get('dnspod.dp_name')
        self.__dp_version = conf.get('dnspod.dp_version')
        self.__dp_mail = conf.get('dnspod.dp_mail')
        self.__dp_domain = conf.get('dnspod.dp_domain')
    def _setDomain(self, domain):
        self.__dp_domain=domain
    def _setToken(self, token):
        self.__dp_token=token
    def _setName(self, name):
        self.__dp_name=name
    def _setVersion(self, version):
        self.__dp_version=version
    def _setMail(self,mail):
        self.__dp_mail=mail

    def modifyRecord(self, subDomain, ip):
        '''Sync DNS record to DNSPod'''
        n='modifyRecord'
        log.write(n,'start')
        recordList=self.getRecordList(subDomain)
        recordId=''
        recordLineId=''
        params={}
        func=''
        if len(recordList)<1:
            log.write(n,'no such sub domain','WARN')
            raise Exception('no such sub domain')
        for record in recordList:
            if record['name']==subDomain:
                recordId=record['id']
                recordLineId=record['line_id']
                break
        if recordId=='':
            log.write(n,'no such sub domain','WARN')
            raise Exception('no such sub domain')
        else:
            params={
                'domain':self.__dp_domain,
                'record_id':recordId,
                'sub_domain':subDomain,
                'record_type':'A',
                'record_line_id':recordLineId,
                'value':ip
            }
            func='Record.Modify'
        result=self.__sendRequest(func,params)
        if result['status']['code']=='1':
            log.write(n,'dns modify success')
            pass
        else:
            log.write(n,result['status']['message'])
            raise Exception(result)
    def getRecordList(self, subDomain=''):
        n='getRecordList'
        log.write(n,'start')
        func = 'Record.List'
        params = {
            'domain':self.__dp_domain
        }
        if subDomain!='':
            params['keyword']=subDomain
        result=self.__sendRequest(func,params)
        if result['status']['code']=='1':
            log.write(n,'success')
            return result['records']
        else:
            raise Exception(result['status']['message'])

    def __sendRequest(self, func = 'User.Detail', params = {}):
        n='__sendRequest'
        log.write(n,'start')
        data = {
           'format': 'json',
           'login_token': self.__dp_token,
           'lang': 'en'
        }
        data = {**data, **params}
        data = parse.urlencode(data).encode('utf-8')
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/json",
            "User-Agent": "%s/%s(%s)" % (self.__dp_name,self.__dp_version,self.__dp_mail)
        }
        req = request.Request(url=self.__dp_base + '/' + func, method='POST', headers=headers, data=data)
        response = request.urlopen(req)
        data = response.read()
        data = json.loads(data)
        return data
