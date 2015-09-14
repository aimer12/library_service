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
from dao.bookdao import BookDao
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
	dao=BookDao(db)
	book1 ={}
	book1['book_titile']= 'introduce to tornado'
	book1['addr']='4-2-7'
	book2 = {'book_title':'learning python', 'author':'liu dw','publisher':'bca','description':'this is a book about basic knowledge of python', 'addr':'4-2-7', 'price':15.21}
	book3 = {'book_title':'Restful Web Service', 'author':'yunjianfei','publisher':'bca','description':'this is a book about restful web service', 'addr':'4-2-34', 'price':34.14}

	book4 = {'author':'aimer yin', 'publisher':'baihualou', 'description':' kanxinqing', 'addr':'7-8-2','price':34.2}

	#ret = dao.insert_by_dict(book3)
	#print 'insert book : %s, ret: %s' % (str(book3),str(ret))

	#h = dao.get_by_bid(1)
	#print 'get by id, ret: %s'% str(h)
	#ret = dao.get_by_title('kim')
	#print 'get by title ,ret: %s' % str(ret)

	#ret = dao.del_by_bid(14)
	ret=dao.update_by_bid(17,book4)
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

	
