#!/usr/bin/env python2.7
#
#
# -*-coding:utf-8 -*-
#  

import string,types,logging
from datetime import date, datetime

def strip_string(ori):
	if ori == None:
		return ori

	ori = str(ori)
	ori = ori.strip("\'")
	ori = ori.strip("\"")
	return ori


def to_int(num):
	if num == None:
		return num
	
	try:
		num = strip_string(num)
		value = int(num)
		return value
	except Exception,ex:
		logging.error("Convert '%s' to Int Error: %s",str(num),str(ex))
		return None

def data_to_int(data):
	pass

def int_to_data(num):
	pass

def json_date_default(obj):
    if isinstance(obj, datetime):
        #return obj.strftime('%Y-%m-%d %H:%M:%S')
        return str(obj)
    elif isinstance(obj, date):
        #return obj.strftime('%Y-%m-%d')
        return str(obj)
    else:
        raise TypeError('%r is not JSON serializable' % obj)


def to_encode(ustr, encoding='utf-8'):  
    if ustr is None:  
        return ''  
    if isinstance(ustr, unicode):  
        return ustr.encode(encoding, 'ignore')  
    else:  
        return str(ustr) 


