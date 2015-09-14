#!/usr/bin/env python2.7
#
#
# -*- coding:utf-8 -*-
#
#

import logging

class BorrowDao:
	def __init__(self,db):
		self.db = db

	def insert_by_dict(self, borrow, replace=False):
		try:
			brw_id=self.db.insert_by_dict('borrow', borrow, replace)
			return brw_id
		except Exception, ex:
			logging.error('insert borrow failed! execption: %s brw: %s',str(ex), str(borrow))
			return None

	def if_exist(self, bookid):
		ret = self.get_by_bookid(bookid)
		if ret != None:
			return True
		return False

	def get_by_bookid(self,bookid):
		sql = "SELECT * FROM borrow WHERE bookid='%s'"%str(bookid)
		return self.db.get(sql)

	def get_by_readerid(self,readerid):
		sql = "SELECT bookid FROM borrow WHERE readerid='%s'"%str(readerid)
		return self.db.query(sql)

	def del_by_bookid(self,bookid):
		try:
			sql = "DELETE FROM borrow WHERE bookid='%s'"%str(bookid)
			ret =self.db.execute(sql)
			return ret
		except Exception, ex:
			logging.error("delete borrow failed! Exception: %s bookid: %s",str(ex), str(bookid))
			return None

	def del_by_returndate(self,returndate):
		try:
			sql = "DELETE FROM borrow WHERE returndate<'%s'"%str(returndate)
			ret =self.db.execute(sql)
			return ret
		except Exception, ex:
			logging.error("delete borrow failed! Exception: %s",str(ex))
			return None


	def update_renew(self,bookid):

		try:
			sql="UPDATE borrow SET renew=1 WHERE bookid='%s'"%str(bookid)
			h=self.db.execute(sql)
			return h
		except Exception, ex:
			logging.error("update renew failed!Exception: %s book_id: %s", str(ex), str(bookid))
			return None

	def update_returndate(self,date,bookid):
		try:
			sql="UPDATE borrow SET returndate='%s' WHERE bookid='%s'"%(str(date),str(bookid))
			ret=self.db.execute(sql)
			return ret
		except Exception, ex:
			logging.error("update returndate failed! Exception: %s book_id: %s", str(ex), str(bookid))
			return None

	def select_overdate(self,returndate):
		sql = "SELECT bookid FROM borrow WHERE returndate<'%s'"%str(returndate)
		return self.db.query(sql)






		



		
			
