# -*- coding:utf-8 -*-

import MeCab
import sys
import io
from io import open
import codecs
import csv
import re

import os.path

import chardet
from chardet.universaldetector import UniversalDetector

import sqlite3

class ScoringClass:
	"""scoring sentense"""
	clueword = None
	keysentence = None

	def openClueWord(self,filename="ClueWord_List.csv"):
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

	def openClueWordDB(self,dbName=u"Wordb.sqlite3",tableName=u"clueword"):
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

	def openSentenceExpression(self,filename="SentenceExpression_List.csv"):
		if ScoringClass.keysentence == None:
			ScoringClass.keysentence = {}
			#read database(SentenceExpression)->dataC
			with io.open(filename,"rt",encoding="utf-8-sig") as file:
				reader = csv.reader(file)
				#readout header
				next(reader)
				#make data exp:importance dict
				for row in reader:
					sentence = row[0].replace("～",".*").decode("utf-8")
					sentence = sentence if sentence.startswith(r".*") else sentence
					ScoringClass.keysentence[sentence] = int(row[2].decode("utf-8"))
			if __name__=="__main__":
				for key in ScoringClass.keysentence.keys():
					print "%s,%d"%(key,ScoringClass.keysentence[key])
		return

	def openSentenceExpressionDB(self,dbName=u"Wordb.sqlite3",tableName=u"SenExp"):
		if ScoringClass.keysentence == None:
			try:
				conn = sqlite3.connect(dbName)
				with conn:
					cr = conn.cursor()
					if cr.execute(u"select count(*) from sqlite_master where type=\"table\" and name=?;",(tableName,)).fetchone()[0] == 0:
						cr.execute(u"create table "+tableName+" (word ntext,importance real);")
						self.openSentenceExpression()
						message = u"insert into "+tableName+" values (:key,:value)"
						cr.executemany(message,self.keysentence.iteritems())
					else :
						ScoringClass.keysentence = {}
						message = u"select * from "+tableName
						for row in cr.execute(message):
							ScoringClass.keysentence[row[0]] = row[1]
			except sqlite3.Error as e:
				print e.message
			except Exception as e:
				print e.message
			finally:
				conn.close()
	#read text
	def scoreSentenceByWord(self,text):
		""" in > text (one sentence)
			out> matching word list[]"""
		matching = []
		m = MeCab.Tagger("-Owakati")
		m.parse('')
		encodeText = text.encode("utf-8")
		node = m.parseToNode(text.encode("utf-8"))
		ans = ""
		node = node.next
		nodeList = []
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

	def scoreSentenceByExp(self,text):
		""" in > text (one sentence)
			out> matching word list[]"""
		matching = []
		for sentence in ScoringClass.keysentence.keys():
			if re.match(sentence,text):
				matching.append(sentence)
		return matching

	def scoreSentenceList(self,textList):
		matchList = []
		for text in textList:
			matchWordList = self.scoreSentenceByWord(text)
			matchExpList = self.scoreSentenceByExp(text)
			matchList.append(matchWordList+matchExpList)
		return matchList

	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		#self.openClueWord()
		self.openClueWordDB(u"WordDB.sqlite3")
		#self.openSentenceExpression()
		self.openSentenceExpressionDB(u"WordDB.sqlite3")

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