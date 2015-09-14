#!/usr/bin/env python2.7
#
#
# -*- coding:utf-8 -*-
#
#

import logging

class ReaderDao:
	def __init__(self,db):
		self.db = db

	def insert_by_dict(self,reader,replace=False):
		try:
			rid=self.db.insert_by_dict('reader',reader,replace)
			return rid
		except Exception,ex:
			logging.error('insert reader failed! execption: %s  reader: %s',str(ex),str(book))
			return None

	def if_exist(self,rid):
		ret = self.get_by_rid(rid)
		if ret != None:
			return True

		return False

	def get_by_rid(self,rid):
		sql = "SELECT * FROM reader WHERE reader_id='" + str(rid)+"'"
		return self.db.get(sql)

	def get_by_rname(self,rname):
		sql = "SELECT * FROM reader WHERE reader_name='" + rname+"'"
		return self.db.get(sql)

	def del_by_rid(self,rid):
		try:
			sql = "DELETE FROM reader WHERE reader_id='"+str(rid)+"'"
			ret = self.db.execute(sql)
			return ret
		except Exception, ex:
			logging.error('delete reader failed! Exception: %s reader_id: %s', str(ex), str(rid))
			return None

	def update_by_rid(self,rid,reader):
		for k,v in reader.items():
			try:
				sql = "UPDATE reader SET %s='%s' WHERE reader_id='%s'" %(str(k),str(v),str(rid))
				ret = self.db.execute(sql)
			except Exception, ex:
				logging.error('update reader failed! Exception: %s reader_id: %s', str(ex), str(rid))
				return None

		return ret

		

