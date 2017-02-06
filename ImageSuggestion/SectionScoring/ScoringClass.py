# -*- coding:utf-8 -*-

import sys
import codecs
import csv
import sqlite3

#External import package to check Unicode parameter
import regex as re

#External import package to check encoding of file
import chardet
from chardet.universaldetector import UniversalDetector

class ScoringClass:
	"""scoring sentense"""
	clueword = None
	keysentence = None

	def openClueWord(self,filename="ClueWord_List.csv"):
		'''	<- filename : filename to read default = ClueWord_List.csv
			 ->No return
			read ClueWord.csv into dict(clueword)'''
		if ScoringClass.clueword == None:
			ScoringClass.clueword = {}
			# read database(ClueWord)->data
			with codecs.open(filename,"r",encoding="utf-8-sig") as file:
				reader = csv.reader(file)
				#readout header
				next(reader)
				#make data word:importance dict
				for row in reader:
					ScoringClass.clueword[row[0].decode("utf-8-sig")] = int(row[2].decode("utf-8-sig"))
		return

	def openClueWordDB(self,dbName=u"WordDB.sqlite3",tableName=u"clueword"):
		'''	<- dbname : filename to read default = WordDB.sqlite3
			<- tableName : tablename to read/write default = clueword
			 ->No return
			read clueword table in Database into dict(clueword)
			if no table or dbfile, read csvfile and save it'''
		if ScoringClass.clueword == None:
			try:
				conn = sqlite3.connect(dbName)
				with conn:
					cr = conn.cursor()
					if cr.execute(u"select count(*) from sqlite_master where type=\"table\" and name=?;",(tableName,)).fetchone()[0] == 0:
						cr.execute(u"create table clueword (word ntext,importance real);")
						self.openClueWord()
						message = u"insert into "+tableName+" values (:key,:value)"
						cr.executemany(message,self.clueword.iteritems())
					else :
						ScoringClass.clueword = {}
						message = u"select * from "+tableName
						for row in cr.execute(message):
							ScoringClass.clueword[row[0]] = row[1]
			except sqlite3.Error as e:
				print e.message
			except Exception as e:
				print e.message

	#read text
	def scoreSentenceByWord(self,text):
		""" in > text (one sentence)
			out> matching word list[]"""
		matching = []
		while node.next:
			nodeList.append((node.surface,node.feature))
			node = node.next
		for node in nodeList:
			try:
				surface = node[0].decode("utf-8-sig")
				feature = node[1].decode("utf-8-sig")
			except UnicodeDecodeError:
				surface = ""
				exit("error! unicode decode error!")
			#searching word
			if surface in ScoringClass.clueword.keys():
				matching.append(surface)
		return matching

	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		#self.openClueWord()
		self.openClueWordDB(u"WordDB.sqlite3")

#てすとプログラム
if __name__ == "__main__":
	print "Start ScorinClass"
	this = ScoringClass()
	textList = []
	filename = "input_main.txt"
	textList = list()
	with codecs.open(filename,mode="r",buffering=-1,encoding="utf-8-sig") as file:
		for line in file.readlines():
			textList.append(re.sub(ur"[\n\r]",u"",line))
	scores = this.scoreSentenceList(textList)
	filename = "output_scorig.txt"
	with codecs.open(filename,"w",encoding="utf-8") as file:
		for tap in zip(textList,scores):
			file.write(tap[0])
			score = tap[1]
			file.write(u"\nmatch:" + unicode(len(score)) + u"\n")
			for match in score:
				file.write(u"\t" + match + ":" + str(ScoringClass.clueword[match] if match in ScoringClass.clueword else ScoringClass.keysentence[match]))
				file.write(u"\n")