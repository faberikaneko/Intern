# -*- coding:utf-8 -*-

import MeCab
import sys
import codecs
import csv
import re

class ScoringClass:
	"""scoring sentense"""
	clueword = None
	keysentence = None

	def openClueWord(self,filename="ClueWord_List.csv"):
		if ScoringClass.clueword == None:
			ScoringClass.clueword = {}
			# read database(ClueWord)->data
			with codecs.open(filename,"r",encoding="utf-8-sig") as f:
				reader = csv.reader(f)
				#readout header
				next(reader)
				#make data word:importance dict
				for row in reader:
					ScoringClass.clueword[row[0].decode("utf-8")] = int(row[2].decode("utf-8"))
		return

	def openSentenceExpression(self,filename="SentenceExpression_List.csv"):
		if ScoringClass.keysentence == None:
			ScoringClass.keysentence = {}
			#データベース読み込む(SentenceExpression)->dataC
			with open(filename,"rt") as f:
				reader = csv.reader(f)
				next(reader)
				#dataCの表現部分：重み辞書を作成
				for row in reader:
					sentence = row[0].replace("～",".*").decode("utf-8")
					sentence = sentence if sentence.startswith(r".*") else sentence
					ScoringClass.keysentence[sentence] = int(row[2].decode("utf-8"))
			for key in ScoringClass.keysentence.keys():
				print "%s,%d"%(key,ScoringClass.keysentence[key])
		return

	#分割する文章を読み込む
	def scoreSentenceByWord(self,text):
		""" in > text (one sentence)
			out> matching word list[]"""
		matching = []
		m = MeCab.Tagger("-Owakati")
		node = m.parseToNode(text.encode("utf-8"))
		ans = ""
		node = node.next
		nodeList = []
		while node.next:
			try:
				surface = node.surface.decode("utf-8")
			except UnicodeDecodeError:
				try:
					surface = node.surface.decode("shift-jis")
				except UnicodeDecodeError:
					surface = node.surface.decode("utf-16")
			nodeList.append(surface)
#			nodeList.append(nono.feature.decode("utf-8"))
#			word = (node.surface.decode("utf-8"),node.feature.decode("utf-8"))
#			ans += "%s %s\n"%word
			if surface in ScoringClass.clueword.keys():
				matching.append(surface)
			node = node.next
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
			matchList.append((textList.index(text),matchWordList+matchExpList))
		return matchList

	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.openClueWord()
		self.openSentenceExpression()

#てすとプログラム
if __name__ == "__main__":
	print "Start ScorinClass"
	this = ScoringClass()
	textList = []
	filename = "imput_scoring.txt"
	try:
		with codecs.open(filename,"r",encoding="utf-8-sig") as file:
			textList = file.readlines()
	except UnicodeDecodeError:
		with codecs.open(filename,"r",encoding="shift-jis") as file:
			textList = file.readlines()
	text = textList[0]
	textList = map(lambda t:t.replace(u"\r\n" or u"\r" or u"\n",""),textList)
	scores = this.scoreSentenceList(textList)
	filename = "output_scorig.txt"
	with open(filename,"wt") as file:
		for score in scores:
			file.write(textList[score[0]])
			file.write("\nmatch:" + str(len(score[1])) + "\n")
			for match in score[1]:
				file.write("\t" + match + ":" + str(ScoringClass.clueword[match] if match in ScoringClass.clueword else ScoringClass.keysentence[match]))
				file.write("\n")
				
	

	#print(key)

	#with open("Output.csv","wb") as f:
	#	writer = csv.DictWriter(f,key)
	#	key_row = {}
	#	for k in key:
	#		key_row[k] = k
	#	writer.writerow(key_row)
	#	for row in data:
	#		writer.writerow(row)