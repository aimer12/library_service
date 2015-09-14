#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#
#

import tornado.web
import json, logging, types, time
from util.config import Config
from util.httpresponse import Response as Resp, ResponseCode as RespCode
from util import tools
from dao.bookdao import BookDao
from dao.readerdao import ReaderDao
from dao.borrowdao import BorrowDao

import util.globalvar as Globalvar
import datetime


class BookHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = self.application.db
		self.bookdao = BookDao(self.db)
		self.Resp = Resp()
	
	def get(self):
		book_id = self.get_argument('book_id', None)
		book_id = tools.to_int(book_id)
		book_title = self.get_argument('book_title', None)
		book_title = tools.strip_string(book_title)
		author = self.get_argument('author', None)
		author = tools.strip_string(author)
		publisher = self.get_argument('publisher', None)
		publisher = tools.strip_string(publisher)

		resp = None
		if book_id != None:
			logging.info("in GET method! Get book by bookid: '%s'", str(book_id))
			book = self.bookdao.get_by_bid(book_id)
			resp = book
		elif book_title != None:
			logging.info("in GET method! Get book by title: '%s'", str(book_title))
			book = self.bookdao.get_by_title(book_title)
			resp = book
		elif author != None:
			logging.info("in GET method! Get book by author: '%s'", str(author))
			book = self.bookdao.get_by_author(author)
			resp = book
		elif publisher != None:
			logging.info("in GET method! Get book by publisher: '%s'", str(publisher))
			book = self.bookdao.get_by_publisher(publisher)
			resp = book
		else:
			logging.info("in GET method! Get All book")
			books = self.bookdao.get_allbook
			resp = books
			
		logging.info("Query result: %s", str(resp))
		
		if resp == None:
			logging.error("There is no record!")
			resp = self.Resp.make_response(code=RespCode.NO_RECORD)
			self.write(resp)
			return
            

		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
		self.write(resp)

	def post(self):
		data = self.request.body
		h = json.loads(data)
		
		logging.info("in  insert method. receive data:%s", str(data))
		book_title = h.get('book_title', None)
		book_title = tools.strip_string(book_title)
		if book_title == None:
			logging.error("there is no parameter 'book_title'!")
			resp = self.Resp.make_response(code = RespCode.NO_PARAMETER, para = 'book_title')
			self.write(resp)
			return
			
		
		addr = tools.strip_string(h.get('addr', None))
		if addr == None:
			logging.error("there is no parameter 'addr'!")
			resp = self.Resp.make_response(code = ReaspCode.NO_PARAMETER, para = 'addr')
			self.write(resp)
			return
			
		author = tools.strip_string(h.get('author', None))
		price = h.get('price',None)
		publisher = tools.strip_string(h.get('publisher', None))
		description = tools.strip_string(h.get('description', None))
		logging.debug("check parameter complete, ready to save in db")
		book = {}
		book['book_title'] = book_title
		book['author'] = author
		book['publisher'] = publisher
		book['description'] = description
		book['addr'] = addr
		book['price'] = price
		
		ret = self.bookdao.insert_by_dict(book)
		if ret == None:
			err_str = "error oncurred when insert into table 'book'"
			logging.error(err_str)
			resp = self.Resp.make_response(code = RespCode.DB_ERROR, err_str = err_str)
			self.write(resp)
			return
			
		logging.info('save book object successed! the book: %s' ,str(book))
		book['book_id'] = ret
		resp = self.Resp.make_response(code = RespCode.SUCCESS, para="add book", content = book)
		self.write(resp)
		
	def delete(self):
		book_id = self.get_argument('book_id', None)
		book_id = tools.strip_string(book_id)
		
		if book_id == None:
			logging.error("there is no parameter 'book_id'!")
			resp = self.Resp.make_response(code = RespCode.NO_PARAMETER, para = 'book_id')
			self.write(resp)
			return
			
		logging.info(" in delete method! delete book by book_id:'%s'.", str(book_id))
		ret = self.bookdao.del_by_bid(book_id)
		err_str = "error oucurred when delete book by id: '%s'" %book_id
		
		
		if ret == None:
			logging.error(err_str)
			resp = self.Resp.make_response(code = RespCode.INVALID_PARAMETER, err_str = err_str)
			self.write(resp)
			return
		
		logging.info("delete book object successed!")
		
		resp = self.Resp.make_response(code = RespCode.SUCCESS, para="delete book")
		self.write(resp)
		
	def put(self):
		data = self.request.body
		h = json.loads(data)
		
		logging.info("in update method! receive data: %s", str(data))
		book_id = h.get('book_id', None)
		book_id = tools.strip_string(book_id)
		
		
		if book_id == None:
			logging.error("there is no parameter 'book_id'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='book_id')
			self.write(resp)
			return
			
		if_exist=self.bookdao.if_exist(book_id)
		if if_exist == False:
			logging.error("the book doesn't existed!")
			resp=self.Resp.make_response(code=RespCode.INVALID_PARAMETER, para='book_id')	
			self.write(resp)
			return
		
		h1 = {}	
		for k, v in h.items():
			if v != None:
				h1[k] = v
				
		ret = self.bookdao.update_by_bid(book_id, h1)
		resp = self.Resp.make_response(code = RespCode.SUCCESS, para='update book')
		self.write(resp)	
		
		
class ReaderHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = self.application.db
		self.readerdao = ReaderDao(self.db)
		self.Resp = Resp()
		
	def post(self):
		data = self.request.body
		h = json.loads(data)
		
		logging.info("in post method. receive data: %s", str(data))
		
		reader_name = h.get('reader_name', None)
		reader_name = tools.strip_string(reader_name)
		if reader_name == None:
			logging.error("there is no parameter 'reader_name'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER,para='reader_name')
			self.write(resp)
			return
			
		sex=tools.to_int(h.get('sex',None))
		age=tools.to_int(h.get('age',None))
		email=tools.strip_string(h.get('email', None))

		logging.debug("check parameters complete, ready to save in db")
		
		reader={}
		reader['reader_name']=reader_name
		reader['sex']=sex
		reader['age']=age
		reader['email']=email
		
		ret = self.readerdao.insert_by_dict(reader)
		if ret == None:
			err_str="error oucurred when insert into table 'reader'"
			logging.error(err_str)
			resp = self.Resp.make_response(code = RespCode.DB_ERROR,err_str=err_str)
			self.write(resp)
			return
			
		logging.info('save reader object successed! the reader: %s', str(reader))

		reader['reader_id']=ret
		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=reader)
		self.write(resp)
		
	def delete(self):
		reader_id=self.get_argument('reader_id',None)
		reader_id=tools.strip_string(reader_id)
		
		if reader_id == None:
			logging.error("there is no parameter 'reader_id'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='reader_id')
			self.write(resp)
			return
		
		logging.info("in delete method! delete reader by reader_id:'%s'.",str(reader_id))
		ret=self.readerdao.del_by_rid(reader_id)
		
		if ret == None:
			err_str="error oucurred when delete reader by id: %s" %reader_id
			logging.error(err_str)
			resp = self.Resp.make_response(code = RespCode.INVALID_PARAMETER,err_str=err_str)
			self.write(resp)
			return
			
		logging.info("delete reader object successed!")
		
		resp = self.Resp.make_response(code = RespCode.SUCCESS,para='delete reader')
		self.write(resp)
		
	def get(self):
		rid = self.get_argument('reader_id', None)
		rid = tools.to_int(rid)
		

		if rid == None:
			logging.error("there is no reader_id!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER)
			self.write(resp)
			return
			
		logging.info("reader detail! readerid:'%s'",str(rid))
		ret=self.readerdao.get_by_rid(rid)
		resp=ret
		logging.info('query result: %s', str(resp))
			
		if resp == None or len(resp) == 0:
			logging.error('there is no record!')
			resp = self.Resp.make_response(code=RespCode.NO_RECORD)
			self.write(resp)

		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
		self.write(resp)
	
		
	def put(self):
		data=self.request.body
		h = json.loads(data)

		logging.info("in update method! receive data: %s", str(data))

		reader_id=h.get('reader_id',None)
		reader_id=tools.strip_string(reader_id)

		if reader_id ==None:
			logging.error("there is no parameter 'reader_id'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='reader_id')
			self.write(resp)
			return

		if_exist=self.readerdao.if_exist(reader_id)
		if if_exist == False:
			logging.error("the book doesn't existed!")
			resp=self.Resp.make_response(code=RespCode.INVALID_PARAMETER, para='READER_id')	
			self.write(resp)
			return


		ret = self.readerdao.update_by_rid(reader_id,h)

		reader = self.readerdao.get_by_rid(reader_id)
		logging.info('update reader object successed! the reader: %s', str(reader))

		resp = self.Resp.make_response(code=RespCode.SUCCESS,content=reader,pare="update reader")
		self.write(resp)
		
		

class BorrowHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = self.application.db
		self.borrowdao = BorrowDao(self.db)
		self.Resp = Resp()
		
	def get(self):
		bookid=self.get_argument('bookid',None)
		readerid=self.get_argument('readerid',None)
		bid=tools.strip_string(bookid)
		rid=tools.strip_string(readerid)
		
		resp = None
		if bid == None and rid == None:
			logging.error("there is no parament bookid or readerid!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER,para='id')
			self.write(resp)
			return
		
		
		if bid != None:
			logging.info("borrow detail! bookid:'%s'",str(bid))
			resp=self.borrowdao.get_by_bookid(bid)
			logging.info('query result: %s', str(resp))
		elif rid != None:
			logging.info("borrow detail! readerid:'%s'",str(rid))
			resp=self.borrowdao.get_by_readerid(rid)
			logging.info('query result: %s', str(resp))
		else:
			return
			
#		bo = tools.to_int(borrow['borrowdate'])
#		re = tools.to_int(borrow['returndate'])
#		bo=datetime.datetime.utcfromstamp(bo)
#		re=	datetime.datetime.utcfromstamp(re)
#		borrow['borrowdate'] = str(bo)
#		borrow['returndate'] = str(re)
			
			
			
		if resp == None or len(resp) == 0:
			logging.error('there is no record!')
			resp = self.Resp.make_response(code=RespCode.NO_RECORD)
			self.write(resp)

		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
		self.write(resp)
		
#		_method = self.get_argument('_method', None)
#		if method == 'lost':
#			self.lost()
#
#	def clear(self):
#		pass
#


	def post(self):
		
		data = self.request.body
		h = json.loads(data)
		
		logging.info("in  post method. receive data:%s", str(data))
		bookid = h.get('bookid', None)
		bookid = tools.strip_string(bookid)
		readerid = h.get('readerid', None)
		readerid = tools.strip_string(readerid)

		resp=None
		if bookid ==None or readerid ==None:
			logging.error("there is no parament bookid or readerid!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER,para='id')
			self.write(resp)
			return
			
		borrow={}
		borrow['bookid']=bookid
		borrow['readerid']=readerid
		
		nowstamp=int(time.time())
		datearray=datetime.datetime.utcfromtimestamp(nowstamp)
		re=datearray+datetime.timedelta(days=31)
		restamp=int(time.mktime(re.timetuple()))
		
		borrow['borrowdate']=nowstamp
		borrow['returndate']=restamp

		ret = self.borrowdao.insert_by_dict(borrow)
		
		if ret == None:
			logging.error("error oucurred when insert into table 'borrow'")
			resp =self.Resp.make_response(code=RespCode.DB_ERROR)
			self.write(resp)
			return


		logging.info("borrow successed! The book: %s", str(bookid))
		borrow['brw_id'] = ret
		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=borrow,para="borrow")
        	self.write(resp)

	def delete(self):
		bookid=self.get_argument('bookid',None)
		bookid=tools.strip_string(bookid)

		resp=None
		if bookid ==None:
			logging.error("there is no parament bookid!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER,para='id')
			self.write(resp)
			return
		
		now=datetime.datetime.now()
		borrow=self.borrowdao.get_by_bookid(bookid)
#		re=datetime.datetime.utcfromtimestamp(borrow['returndate'])
#		delta=re-now
#		days=getattr(delta,'days')
#		if days < 0:
#			logging.error("this book is delay for %s days",str(abs(days)))
#			resp = self.Resp.make_response(code=Resp.DELAY,para=days)
#			self.write(resp)
			
		logging.info("delete borrow book %s",str(bookid))
		ret=self.borrowdao.del_by_bookid(bookid)

		logging.info("delete successed!")

		resp = self.Resp.make_response(code=RespCode.SUCCESS, para="return")
		self.write(resp)
		
		
	def put(self):
		data = self.request.body
		h = json.loads(data)
		
		bookid = h.get('bookid', None)

		if bookid == None:
			logging.error("there is no input!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER,pare= 'bookid')
			self.write(resp)

			return
#sql = "SELECT renew FROM borrow WHERE bookid='%s'"%str(bookid)
#		ret=self.db.get(sql)
#		if ret['renew'] == 0:

#		logging.info('renew book id:%s',str(bookid))
#		ret = self.borrowdao.update_renew(bookid)


			#####add a month###
		re=self.borrowdao.get_by_bookid(bookid)
		restamp=re['returndate']
		datearray=datetime.datetime.utcfromtimestamp(restamp)
		re1=datearray+datetime.timedelta(days=31)
		re1stamp=int(time.mktime(re1.timetuple()))
		ret=self.borrowdao.update_returndate(re1stamp,bookid)
		
		logging.info("renew success! bookid:'%s'",str(bookid))
		resp = self.Resp.make_response(code=RespCode.SUCCESS, para="renew")
		self.write(resp)
			
		
			
