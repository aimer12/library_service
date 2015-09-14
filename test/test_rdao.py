#!/usr/bin/env python2.7
#
#
#  -*- coding:utf-8 -*-
#
#
#

import json, logging
from util.config import Config
import util.globalvar as GlobalVar
from util import torndb
from dao.readerdao import ReaderDao
import types


CONF_FILE = "conf/svc.conf"

def parse_config(conf_file):
	conf = Config(conf_file)
	conf.load_conf()

def init_logging():
	sh = logging.StreamHandler()
	logger = logging.getLogger()
	logger.setLevel(Config.log_level)

	formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
	sh.setFormatter(formatter)

	logger.addHandler(sh)
	logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))

def test_dao(db):
	dao=ReaderDao(db)
	re1 ={}
	re1['reader_name']= 'dw'
	re1['sex']='2'
	re2= {'reader_name':'yin','sex':'1','email':'chi@de','type':'1'}
	

	re3 = {'age':'13','type':'0'}

	#ret = dao.insert_by_dict(re2)
	#print 'insert reader : %s, ret: %s' % (str(re1),str(ret))

	#h = dao.get_by_rname('dw')
	#print 'get by reader_name, ret: %s'% str(h)
    #ret = dao.get_by_title('python')
	#print 'get by title ,ret: %s' % str(ret)

	ret = dao.del_by_rid(2)
	#ret=dao.update_by_rid('2',re3)
	print ret

def main():
	#########parse and load config file###########
	parse_config(CONF_FILE)
	
	init_logging()
	mysql_host= Config.db_host + ':' + str(Config.db_port)
	db = torndb.Connection(
		host=mysql_host, database=Config.db_name,
		user=Config.db_user, password=Config.db_pass
	)

	######################init db const value############
	test_dao(db)

if __name__ == "__main__" :
	main()

	
