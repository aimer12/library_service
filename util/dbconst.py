#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#   Author  :   YunJianFei
#   E-mail  :   yunjianfei@126.com
#   Date    :   2014/02/25
#   Desc    :   Test db
#
#   edit by Aimer YIN

class Table:
	table = None
	db = None

	def __init__(self,db,tablename):
    	Table.table = tablename
		Table.db=db

	def TableFields(self):
        TableFields = Table.db.get_fields_str(Table.table)

	def TableSelectSql(self):
        TableSelectSql.Table = Table.db.get_select_sql(Table.table)
