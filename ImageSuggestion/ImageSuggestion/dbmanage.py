# -*- encode:utf-8 -*-

import sys

import codecs

import sqlite3

from operator import add

def openDB(dbName):
	return packedSQL(sqlite3.connect(dbName))
	
class packedSQL:
	''' overraped sqlite3 '''
	def __init__(self,dbConn):
		self.db = dbConn
		self.cr = dbConn.cursor()

	def createTable(self,tableName,tableHeader):
		try:
			row = self.cr.execute("select count(*) from sqlite_master where type=\"table\" and name=?",(tableName,)).fetchone()
			hreadMes = ()
			if row == None or row[0] == 0:
				tableHeader = list(map(lambda a:" ".join(a),tableHeader))
				message = u"create table "+tableName+"("+",".join(tableHeader)+");"
				self.db.execute(message)
				return True
			else:
				return False
		except sqlite3.Error as e:
			print e.message
			exit(-1)

	def search(self,tableName,what=u"*",where=None):
		ans = []
		message = u"select "+what+" from "+tableName+[" where ? ",""][where==None] + ";"
		for row in self.db.execute(message):
			ans.append(row)
		return ans

	def insert(self,tableName,valueList):
		try:
			message =u"insert into "+tableName+" values("+",".join(["?"]*len(valueList))+");"
			self.db.execute(message,valueList)
		except sqlite3.Error as e:
			print e.message
			exit(-1)
if __name__ == "__main__":
	print "hello sqlite3"
	db = openDB("test.db")
	tableName = u"word"
	tableHeader = [(u"name",u"ntext"),(u"id",u"int"),]
	if db.createTable(tableName,tableHeader):
		print "create table \"texts\""
	else:
		print "has already created"
	db.insert(tableName,(u"the answer",42))
	l = db.search(tableName)
	print l