#!/usr/bin/env python2.7
#
#
# -*- coding:utf-8 -*-
#

import time, signal, logging, os
import urllib
import urllib2
import tornado.httpclient
import tornado
import json
from tornado.httpclient import AsyncHTTPClient

def make_qs(query_args):
	kv_pairs = []
	for (key, val) in query_args.iteritems():
		if val:
			if isinstance(val, list):
				for v in val:
					kv_pairs.append((key,v))
			else:
				kv_pairs.append((key, val))

	qs = urllib.urlencode(kv_pairs)
	return qs

def sig_handler(sig, frame):
	logging.warning('Caught signal: %s', sig)
	tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    logging.info('Will shutdown in %s seconds ...', 2)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 2

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')
    stop_loop()

def handle_request(response):
	if response.error:
		print "Error:",response.error
	else:
		print "------------------------------------------------------"
		print "requset url:" + response.request.url
		print "\nMethod:" + response.request.method
		if response.request.body:
			print "\nrequest body: \n" + json.dumps(json.loads(response.request.body),indent=2)
			
		print "\nResponse: "
		body = response.body
		resp = json.loads(body)
		print json.dumps(resp, indent = 2)
		
def test(http_client):
	book = {}
	book["book_id"] =2
	book['book_title']="change python"
	book['addr']="3-4-7"

	#url = "http://127.1:9999/bookmanage"
	#http_client.fetch(url, handle_request, method ='GET')

	#url = "http://127.1:9999/bookmanage"
	#http_client.fetch(url, handle_request, method='POST', body=json.dumps(book))
	
	#url = "http://127.1:9999/bookmanage?book_id=2"
	#http_client.fetch(url, handle_request, method='DELETE')
	
	#url = "http://127.1:9999/bookmanage"
	#http_client.fetch(url, handle_request, method = 'PUT', body = json.dumps(book))
	
	reader = {}
	reader['reader_id'] = '5'
	reader['reader_name'] = 'mingtian'
	reader['email'] = 'heihei'
	
	#url = "http://127.1:9999/readermanage"
	#http_client.fetch(url,handle_request, method='PUT',body=json.dumps(reader))
	
	#url = "http://127.1:9999/readermanage"
	#http_client.fetch(url,handle_request, method='POST',body=json.dumps(reader))
	
	#url = "http://127.1:9999/readermanage?reader_id=5"
	#http_client.fetch(url,handle_request, method='GET')
	
	#url = "http://127.1:9999/readermanage?reader_id=5"
	#http_client.fetch(url,handle_request, method='DELETE')
	
	borrow = {}
	borrow['bookid']=3
#	borrow['readerid']=1
	
	#url="http://127.1:9999/borrow"
	#http_client.fetch(url, handle_request, method="POST",body=json.dumps(borrow))
	#url = "http://127.1:9999/borrow?readerid=1"
	#http_client.fetch(url, handle_request, method="GET")
#	url = "http://127.1:9999/borrow"
#	http_client.fetch(url, handle_request, method="PUT",body=json.dumps(borrow))

	url = "http://127.1:9999/borrow?bookid=3"
	http_client.fetch(url, handle_request, method="DELETE")


def main():
	signal.signal(signal.SIGTERM, sig_handler)
	signal.signal(signal.SIGINT, sig_handler)

	http_client = AsyncHTTPClient()

	test(http_client)

	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()


