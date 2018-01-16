#! /usr/bin/python
#-*- coding:utf-8 -*-
import json
from pprint import pprint
with open('config.json') as json_file:
    data = json.load(json_file)

def get(key_chain):
    key_chain = key_chain.split('.')
    tmp = data
    for key in key_chain:
        tmp = tmp[key]
    return tmp
