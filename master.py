#!/usr/bin/env python2.7
#
#
# -*- coding:utf-8 -*-
#

import string, os, sys, logging, signal, time
import tornado.httpserver
import tornado.ioloop
import tornado.web

from util.options import define, options
from util.config import Config
from util import torndb
import util.globalvar as GlobalVar

from service.lib import  BookHandler, ReaderHandler, BorrowHandler

MODULE='master'
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN=3

CONF_FILE='conf/svc.conf'

define('port',default=None, help="run server on a specific port, must imput",type=int)

def parse_config(conf_file):
	conf = Config(conf_file)
	conf.load_conf()

def init_logging(port):
	log_file=MODULE+"."+str(port)+".log"
	logger=logging.getLogger()
	logger.setLevel(Config.log_level)

	fh = logging.handlers.TimedRotatingFileHandler(os.path.join(Config.log_path,log_file),when='D',backupCount=10)
	sh = logging.StreamHandler()

	formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
	fh.setFormatter(formatter)
	sh.setFormatter(formatter)

	logger.addHandler(fh)
	logger.addHandler(sh)
	logging.info("Current log level is: %s",logging.getLevelName(logger.getEffectiveLevel()))

def sig_handler(sig,frame):
	logging.warning('Caught signal: %s',sig)
	tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
	logging.info('stopping http server')
	http_server.stop()

	logging.info('Master will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
	io_loop = tornado.ioloop.IOLoop.instance()

	deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

	def stop_loop():
		now = time.time()
		if now < deadline and (io_loop._callbacks or io_loop._timeouts):
			io_loop.add_timeout(now + 1, stop_loop)
		else:
			io_loop.stop()
			GlobalVar.get_db_handle().close()
			#GlobalVar.get_mq_client().disconnect()
			logging.info('Shutdown')

	stop_loop()

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("this is library system Master!")

class Application(tornado.web.Application):
	def __init__(self):
		settings = dict(
			debug=True,
		)

		handlers = [
			(r"/", MainHandler),
			(r"/reader",ReaderHandler),
			(r"/book",BookHandler),
			(r"/borrow", BorrowHandler),
		]

		mysql_host =Config.db_host+":"+str(Config.db_port)
		self.db = torndb.Connection(
			host = mysql_host, database = Config.db_name,
			user = Config.db_user, password = Config.db_pass
		)
		
		GlobalVar.set_db_handle(self.db)

		super(Application,self).__init__(handlers, **settings)

def main():
	options.parse_command_line()

	if options.port == None:
		options.print_help()
		return
	
	parse_config(CONF_FILE)

	init_logging(options.port)

	logging.info("Test info:Master start!")
	logging.error("Test error:Master start!")
	logging.debug("Test debug:Master start!")

	global http_server

	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)

	signal.signal(signal.SIGTERM, sig_handler)
	signal.signal(signal.SIGINT, sig_handler)

	tornado.ioloop.IOLoop.instance().start()
	logging.info('Exit Master')

if __name__ == "__main__":
	main()



