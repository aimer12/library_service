#!/usr/bin/env python2.7
#
#
# -*- coding:utf-8 -*-
#
#



import logging

class BookDao:
	def __init__(self, db):
		self.db=db

	def insert_by_dict(self, book, replace=False):
		try:
			bid=self.db.insert_by_dict("book", book, replace)
			return bid
		except Exception,ex:
			logging.error("insert book failed! exception: %s  book: %s", str(ex), str(book))
			return None

	def if_exist(self, bid):
		ret = self.get_by_bid(bid)
		if ret != None:
			return True 
			
		return False

	def get_by_bid(self,bid):
		sql = "SELECT * FROM book WHERE book_id = '" +str(bid) +"'"
		return self.db.get(sql)

	def get_by_title(self,title):
		sql = "SELECT * FROM book WHERE book_title LIKE '%%"+title+"%%'"
		return self.db.query(sql)

	def get_by_author(self,author):
		sql =  "SELECT * FROM book WHERE author LIKE '%%" + author + "%%'"
		return self.db.query(sql)

	def get_by_publisher(self,publisher):
		sql = "SELECT * FROM book WHERE publisher LIKE '%%" +publisher + "%%'"
		return self.db.query(sql)
	
	def get_allbook(self):
		sql = "SELECT * FROM book"
		return self.db.query(sql)

	def del_by_bid(self,bid):
		try:
			sql = "DELETE FROM book WHERE book_id = '" + str(bid) + "'"
			ret = self.db.execute(sql)
			return ret
		except Exception, ex:
			logging.error("delete book failed! Exception: %s  book_id: %s", str(ex), str(bid))
			return None 

	def update_by_bid(self, bid, book):
		for k, v in book.items():
			try:
				sql = "UPDATE book SET  %s='%s' WHERE book_id= %s" % (str(k),str(v),str(bid)) 
				ret =self.db.execute(sql)
			except Exception, ex:
				logging.error("updata book failed! Exception: %s book_id: %s, item: %s", str(ex), str(bid) ,str(k))
				return None
		
		return ret
				
		


