#!/usr/bin/env python2.7
#
#
#
#  -*- coding:utf-8 -*-
#
#

import tornado.web
import json, logging,types, time, datetime
from util.httpresponse import Response as Resp, ResponseCode as Respcode
from util import tools
from dao.bookdao import BookDao
from dao.readerdao import ReaderDao
from dao.borrowdao import BorrowDao

import util.globalvar as Globalvar

class UserHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = self.application.db
		self.bookdao=BookDao(self.db)
		self.readerdao=ReaderDao(self.db)
		self.borrowdao=BorrowDao(self.db)
		self.Resp=Resp()
		
	def search(self):
		se=self.get_argument('book',None)
		se=tools.strip_string(se)
		
		resp = []
		if se != None:
			logging.info("in search method! get search input:'%s'",str(se))
			ret=self.bookdao.get_by_title(se)
			resp.extend(ret)
			ret=self.bookdao.get_by_auther(se)
			resp.extend(ret)
			ret=self.bookdao.get_by_publisher(se)
			resp.extend(ret)

			logging.info('query result: %s', str(resp))

		else:
			logging.error("there is no input!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER,pare= 'input')
			self.write(resp)
			return

		if resp == None or len(resp) == 0:
			logging.error('there is no record!')
			resp = self.Resp.make_response(code=RespCode.No_RECORD)
			self.write(resp)

		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
		self.write(resp)

	
	def getbybid(self):
		bid=self.get_argument('book_id',None)
		bid=tools.strip_string(bid)

		resp=None
		if bid != None:
			logging.info("bookdetail! bookid:'%s'",str(bid))
			ret=self.bookdao.get_by_bid(bid)
			resp=ret
			h=self.borrowdao.if_exist(bid)
			if h==True:
				resp['onsheet']='no'
			else:
				resp['onsheet']='yes'

			logging.info('query result: %s', str(resp))
		else:
			logging.error("there is no input!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER,pare= 'bid')
			self.write(resp)
			return



		if resp == None or len(resp) == 0:
			logging.error('there is no record!')
			resp = self.Resp.make_response(code=RespCode.No_RECORD)
			self.write(resp)

		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
		self.write(resp)


	def searchbyrid(self):
		rid = self.get_argument('readerid',None)
		rid = tools.strip_string(rid)
		

		resp=None
		if readerid != None:
			logging.info("in searchbyrid method! get reader by readerid:'%s'",str(rid))
			ret= self.readerdao.get_by_rid(rid)
			resp=ret
			books=self.borrowdao.get_by_readerid(rid)
			resp["books"]=books

			logging.info('query result: %s', str(resp))


			
		if resp == None or len(resp) == 0:
			logging.error('there is no record!')
			resp = self.Resp.make_response(code=RespCode.No_RECORD)
			self.write(resp)

		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
		self.write(resp)

	def renew(self):
		bookid=self.get_argument('bookid',None)
		bookid=self.tools.strip_string(bookid)

		if bookid == None:
			logging.error("there is no input!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER,pare='bid')
			self.write(resp)
			return


		logging.info('renew book id:%s',str(bookid))
		ret=self.borrowdao.update_renew(bookid)

		if ret:
			#####add a month###
			re=self.borrowdao.get_by_bookid(bookid)
			restamp=re['returndate']
			datearray=datetime.datetime.utcfromtimestamp(restamp)
			re1=datearray+datetime.timedelta(days=31)
			re1stamp=int(time.mktime(re1.timetuple()))
			ret=update_returndate(re1stamp,bookid)
		
			logging.info("renew success! bookid:'%s'",str(bookid))
		else:
			logging.error("Fail! already done before.")
			resp = self.Resp.make_response(code=RespCode.HAS_EXISTED)
			self.write(resp)

		
			
	
		resp = self.Resp.make_response(code=RespCode.SUCCESS)
		self.write(resp)

class BookHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = self.application.db
		self.bookdao=BookDao(self.db)
		self.readerdao=ReaderDao(self.db)
		self.borrowdao=BorrowDao(self.db)
		self.Resp=Resp()

	def insert(self):
		data = self.request.body
		h = json.loads(data)

		logging.error("in insert method. receive data:%s", str(data)) 

		book_title = h.get('book-title',None)
		book_title = tools.strip_string(book_title)
		if book_title == None:
			logging.error("there is no parameter 'book_title'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER,para='book_title')
			self.write(resp)
			return

		addr=tools.strip_string(h.get(addr,None))
		if addr == None:
			logging.error("there is no parameter 'addr'!")
			resp = self.Reap.make_response(code = RespCode.NO_PARAMETER,para='addr')
			self.write(resp)
			return

		author=tools.strip_string(h.get('author',''))
		publisher=tools.strip_string(h.get('publisher',''))
		description=tools.strip_string(h.get('description',''))
		price=float(h.get('price',0))

		logging.debug("check parameters complete, ready to save in db")

		book={}
		book['book_title']=book_title
		book['author']=author
		book['publiser']=publisher
		book['description']=description
		book['addr']=addr
		book['price']=price

		ret = self.bookdao.insert_by_dict(book)
		if ret == None:
			err_str="error oucurred when insert into table 'book'"
			logging.error(err_str)
			resp = self.Resp.make_response(code = RespCode.DB_ERROR,err_str=err_str)
			self.write(resp)
			return

		logging.info('save book object successed! the book: %s', str(book))

		book['book_id']=ret
		resp = self.Resp.make_response(code=RespCode.SUCCESS,content=book)
		self.write(resp)

	def update(self):
		data=self.request.body
		h = json.loads(data)

		logging.info("in update method! receive data: %s", str(data))

		book_id=h.get('book_id',None)
		book_id=tools.strip_string(book_id)

		book_title=tools.strip_string(h.get('book_title',None))
		if book_id ==None:
			logging.error("there is no parameter 'book_id'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='book_id')
			self.write(resp)
			return

		if_exist=self.bookdao.if_exist(book_id)
		if if_exist == False:
			logging.error("the book doesn't existed!")
			resp=self.Resp.make_response(code=RespCode.NO_RECORD, para='book_id')	
			self.write(resp)
			return


		ret=self.bookdao.update_by_bid(book_id,h)
		resp=self.Resp.make_response(code=RespCode.SUCCESS)
		self.write(resp)

 
#		get=self.bookdao.get_by_bid(book_id)
#		book={}
#		book['addr']=tools.strip_string(h.get(addr,get['addr']))
#		book['author']=tools.strip_string(h.get('author',get['author']))
#		book['publisher']=tools.strip_string(h.get('publisher',get['pubulisher']))
#		book['description']=tools.strip_string(h.get('description',get['description']))
#		book['price']=float(h.get('price',get['price']))

#		ret=self.bookdao.update_by_bid(book_id,book)

#		ret always be 0,so can not classify it, it is problem

		

	def getbybid(self):

		book_id=self.get_argument('book_id',None)
		book_id=tools.strip_string(book_id)
		if book_id ==None:
			logging.error("there is no parameter 'book_id'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='book_id')
			self.write(resp)
			return

		logging.info("in getbybid method. get book by id: '%s'",str(book_id))
		ret=self.bookdao.get_by_bid(book_id)
		resp =ret

		if resp == None or len(resp)== 0:
			logging.error("there is no record!")
			resp = self.Resp.make_response(code=RespCode.NO_RECORD)
			self.write(resp)
			return

		resp = self.Resp.make_response(code=RespCode.SUCCESS,content=resp)
		self.write(resp)

	def getall(self):


		logging.info("in get all book method :")
		ret=self.bookdao.get_allbook()
		resp =ret

		if resp == None or len(resp)== 0:
			logging.error("there is something wrong!")
			resp = self.Resp.make_response(code=RespCode.DB_ERROR)
			self.write(resp)
			return

		resp = self.Resp.make_response(code=RespCode.SUCCESS,content=resp)
		self.write(resp)

	def delbybid(self):
		book_id=self.get_argument('book_id',None)
		book_id=tools.strip_string(book_id)
		
		if book_id == None:
			logging.error("there is no parameter 'book_id'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='book_id')
			self.write(resp)
			return
		
		logging.info("in delete method! delete book by book_id:'%s'.",str(book_id))
		ret=self.bookdao.del_by_bid(bid)

####same problem as before , db.excute() return 0 whether is succuss or fail###

		'''
		if ret == None:
		resp= self.Resp.make_response(code = RespCode.

		'''
		logging.info("delete book object successed!")

		resp = self.Resp.make_response(code=RespCode.SUCCESS)
		self.write(resp)


class ReaderHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = self.application.db
		self.bookdao=BookDao(self.db)
		self.readerdao=ReaderDao(self.db)
		self.borrowdao=BorrowDao(self.db)
		self.Resp=Resp()
	
	def insert(self):
		data = self.request.body
		h = json.loads(data)

		logging.error("in insert method. receive data:%s", str(data)) 

		reader_name = h.get('reader_name',None)
		reader_name = tools.strip_string(reader_name)
		if reader_name == None:
			logging.error("there is no parameter 'reader_name'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER,para='reader_name')
			self.write(resp)
			return

		sex=tools.to_int(h.get('sex',None))
		age=tools.to_int(h.get('age',None))
		email=tools.strip_string(h.get('email',''))

		logging.debug("check parameters complete, ready to save in db")

		reader={}
		reader['reader_name']=reader_name
		reader['sex']=sex
		reader['age']=age
		reader['email']=email

		ret = self.readerdao.insert_by_dict(reader)
#########insert fail return None?###############
		if ret == None:
			err_str="error oucurred when insert into table 'reader'"
			logging.error(err_str)
			resp = self.Resp.make_response(code = RespCode.DB_ERROR,err_str=err_str)
			self.write(resp)
			return

		logging.info('save reader object successed! the reader: %s', str(reader))

		reader['reader_id']=ret
		resp = self.Resp.make_response(code=RespCode.SUCCESS,content=reader)
		self.write(resp)

	def delbyrid(self):
		reader_id=self.get_argument('reader_id',None)
		reader_id=tools.strip_string(reader_id)
		
		if reader_id == None:
			logging.error("there is no parameter 'reader_id'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='reader_id')
			self.write(resp)
			return
		
		logging.info("in delete method! delete reader by reader_id:'%s'.",str(reader_id))
		ret=self.readerdao.del_by_rid(bid)

		'''
		if ret == None:
		resp= self.Resp.make_response(code = RespCode.

		'''
		logging.info("delete reader object successed!")

		resp = self.Resp.make_response(code=RespCode.SUCCESS)
		self.write(resp)

	def update(self):
		data=self.request.body
		h = json.loads(data)

		logging.info("in update method! receive data: %s", str(data))

		reader_id=h.get('reader_id',None)
		reader_id=tools.strip_string(reader_id)

		reader_name=tools.strip_string(h.get('reader_name',None))
		if reader_id ==None:
			logging.error("there is no parameter 'reader_id'!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='reader_id')
			self.write(resp)
			return

		if_exist=self.readerdao.if_exist(reader_id)
		if if_exist == False:
			logging.error("the book doesn't existed!")
			resp=self.Resp.make_response(code=RespCode.NO_RECORD, para='book_id')	
			self.write(resp)
			return


		ret=self.readerdao.update_by_rid(reader_id,h)


#		get=self.bookdao.get_by_bid(book_id)
#		book={}
#		book['addr']=tools.strip_string(h.get(addr,get['addr']))
#		book['author']=tools.strip_string(h.get('author',get['author']))
#		book['publisher']=tools.strip_string(h.get('publisher',get['pubulisher']))
#		book['description']=tools.strip_string(h.get('description',get['description']))
#		book['price']=float(h.get('price',get['price']))


#		ret=self.bookdao.update_by_bid(book_id,book)

        #ret return
		reader=self.readerdao.get_by_rid(reader_id)
		logging.info('update reader object successed! the reader: %s', str(reader))

		resp = self.Resp.make_response(code=RespCode.SUCCESS,content=reader)
		self.write(resp)

	def getbyrid(self):
		rid=self.get_argument('readerid',None)
		rid=tools.strip_string(rid)

		resp=None
		if rid != None:
			logging.info("reader detail! readerid:'%s'",str(rid))
			ret=self.readerdao.get_by_rid(rid)
			resp=ret
			logging.info('query result: %s', str(resp))
		else:
			logging.error("there is no input!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER,pare= 'input')
			self.write(resp)
			return

		if resp == None or len(resp) == 0:
			logging.error('there is no record!')
			resp = self.Resp.make_response(code=RespCode.No_RECORD)
			self.write(resp)

		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
		self.write(resp)


class BorrowHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = self.application.db
		self.bookdao=BookDao(self.db)
		self.readerdao=ReaderDao(self.db)
		self.borrowdao=BorrowDao(self.db)
		self.Resp=Resp()

	def borrow(self):
		bookid=self.get_argument('bookid',None)
		readerid=self.get_argument('readerid',None)
		bookid=tools.strip_string(bookid)
		readerid=tools.strip_string(readerid)

		resp=None
		if bookid ==None or readerid ==None:
			logging.error("there is no parament bookid or readerid!")
			resp = self.Resp.make_response(code=RespCode.NO_PARAMETER,para='id')
			self.write(resp)
			return
		
		'''check readerid bookid exist and borrow exist ...'''

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
			resp =self.Resp.make_response(code=RespCode.DB_ERROE)
			self.write(resp)
			return

		else:
			logging.info("borrow successed! The book: %s", str(bookid))
        	borrow['brw_id'] = ret
        	resp = self.Resp.make_response(code=RespCode.SUCCESS, content=borrow)
        	self.write(resp)
			


	def returnbook(self):
		
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
		re=datetime.datetime.utcfromtimestamp(borrow['returndate'])
		delta=re-now
		day=getattr(delta,'days')
		if day < 0:
			punish=0.5*abs(day)

			logging.error("this book is delay and pay for %s yuan!",str(punish))
			resp = self.Resp.make_response(code=RespCode.RETURN,para='punish')
			self.write(resp)

		logging.info("delete borrow book %s",str(bookid))
		ret=self.borrowdao.del_by_bookid(bookid)

		logging.info("delete successed!")

		resp = self.Resp.make_response(code=RespCode.SUCCESS)
		self.write(resp)


	def renew(self):
		bookid=self.get_argument('bookid',None)
		bookid=self.tools.strip_string(bookid)

		if bookid == None:
			logging.error("there is no input!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER,pare= 'input')
			self.write(resp)
			return
			


		logging.info('renew book id:%s',str(bookid))
		ret=self.borrowdao.update_renew(bookid)

#	if ret:
#			logging.info("renew success! bookid:'%s'",str(bookid)
#		else:
#			logging.error("Fail! already done before.")
#			resp = self.Resp.make_response(code=RespCode.HAS_EXISTED)
#			self.write(resp)
#
#add a month
		re=self.borrowdao.get_by_bookid(bookid)
		restamp=re['returndate']
		datearray=datetime.datetime.utcfromtimestamp(restamp)
		re1=datearray+datetime.timedelta(days=31)
		re1stamp=int(time.mktime(re1.timetuple()))
		ret=update_returndate(re1stamp,bookid)
		
			
	
		resp = self.Resp.make_response(code=RespCode.SUCCESS)
		self.write(resp)


	def getbybid(self):
		bid=self.get_argument('book_id',None)
		bid=tools.strip_string(bid)

		resp=None
		if bid != None:
			logging.info("borrowdetail! bookid:'%s'",str(bid))
			ret=self.borrowdao.get_by_bid(bid)
			resp=ret
			logging.info('query result: %s', str(resp))
		else:
			logging.error("there is no input!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER,pare= 'bid')
			self.write(resp)
			return



		if resp == None or len(resp) == 0:
			logging.error('there is no record!')
			resp = self.Resp.make_response(code=RespCode.No_RECORD)
			self.write(resp)

		resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
		self.write(resp)

		



	def lost(self):

		bid=self.get_argument('book_id',None)
		bid=tools.strip_string(bid)

		if bid != None:
			h=self.bookdao.get_by_bid(bid)
			price=h['price']
			logging.info("lost bookid:'%s',pay for $%s",str(bid),str(price))
			ret=self.bookdao.del_by_bid(bid)		
		else:
			logging.error("there is no input!")
			resp=self.Resp.make_response(code=RespCode.NO_PARAMETER,pare= 'bid')
			self.write(resp)
			return

		resp = self.Resp.make_response(code=RespCode.SUCCESS)
		self.write(resp)




	def clearlist(self):
		pass



		
			
			

		


		




