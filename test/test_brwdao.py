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
from dao.borrowdao import BorrowDao
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
	dao=BorrowDao(db)
	re1 ={}
	re1['bookid']= '3'
	re1['readerid']=3
	re1['borrowdate']='150712'
	re1['returndate']='150812'	
	re2= {}
	re3 = {}

	#ret = dao.insert_by_dict(re1)
	#ret=dao.get_by_readerid(1)
	#ret=dao.update_renew(1)
	#ret=dao.update_returndate(150803,1)
	#ret=dao.select_overdate(150730)
	#ret=dao.del_by_bookid(3)
	ret=dao.del_by_returndate(150830)
	#print 'insert list : %s, ret: %s' % (str(re1),str(ret))

	#h = dao.get_by_rname('dw')
	#print 'get by reader_name, ret: %s'% str(h)
    #ret = dao.get_by_title('python')
	#print 'get by title ,ret: %s' % str(ret)

	#ret = dao.del_by_rid(2)
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

	
