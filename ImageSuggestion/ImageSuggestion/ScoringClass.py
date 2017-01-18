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
			#read database(SentenceExpression)->dataC
			with open(filename,"rt") as f:
				reader = csv.reader(f)
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
		try:
			surface = node.surface.decode("utf-8")
		except UnicodeDecodeError:
			try:
				surface = node.surface.decode("shift-jis")
			except UnicodeDecodeError:
				surface = ""
#					exit("error! unicode decode error!")
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
			matchList.append(matchWordList+matchExpList)
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
	filename = "input_main.txt"
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

## -*- coding:utf-8 -*-

#import MeCab
#import sys
#import codecs
#import csv

#class ScoringClass:
#	"""scoring sentense"""
#	clueword = None
#	keysentence = None

#	def openClueWord(self,filename="ClueWord_List.csv"):
#		if ScoringClass.clueword == None:
#			ScoringClass.clueword = {}
#			# データベースを読み込む(ClueWord)->data
#			with open(filename,"rt") as file:
#				reader = csv.reader(file)
#				#ヘッダ行の読み飛ばし
#				next(reader)
#				#dataの表現部分：重み辞書を作成
#				for row in reader:
#					ScoringClass.clueword[row[0].decode("utf-8")] = int(row[2].decode("utf-8"))
#		return

#	def openSentenceExpression(self,filename="SentenceExpression_List.csv"):
#		if ScoringClass.keysentence == None:
#			ScoringClass.keysentence = {}
#			#データベース読み込む(SentenceExpression)->dataC
#			with open(filename,"rt") as file:
#				reader = csv.reader(file)
#				next(reader)
#				#dataCの表現部分：重み辞書を作成
#				for row in reader:
#					ScoringClass.keysentence[row[0].replace("～","*").decode("utf-8")] = int(row[2].decode("utf-8"))
#		return

#	#分割する文章を読み込む
#	def scoreSentence(self,text):
#		point = 0
#		m = MeCab.Tagger("-Owakati")
#		node = m.parseToNode(text)
#		ans = ""
#		node = node.next
#		while node.next:
#			word = (node.surface.decode("utf-8"),node.feature.decode("utf-8"))
#			ans += "%s %s\n"%word
#			if word[0] in ScoringClass.clueword.keys():
#				point += ScoringClass.clueword[word[0]]
##				print"%s %d"%(node.surface.decode("utf-8"),ScoringClass.clueword[word[0]])
#			node = node.next
#		print point
#		return point

#	def scoreSentenceList(self,textList):
#		scoreList = []
#		for text in textList:
#			score = self.scoreSentence(text)
#			scoreList.append((text,score))
#		return scoreList

#	def __init__(self):
#		self.openClueWord()
#		self.openSentenceExpression()

##てすとプログラム
#if __name__ == "__main__":
#	print "Start ScorinClass"
#	this = ScoringClass()
#	textList = []
#	filename = "text.txt"
#	with open(filename,"rt") as f:
#		textList = f.readlines()
#	scores = this.scoreSentenceList(map(lambda t : t.replace("\n","") , textList))
#	filename = "output.txt"
#	with open(filename,"wt") as f:
#		for score in scores:
#			f.write(score[0] + ":" + str(score[1]) + "\n")
	

#	#print(key)

#	#with open("Output.csv","wb") as f:
#	#	writer = csv.DictWriter(f,key)
#	#	key_row = {}
#	#	for k in key:
#	#		key_row[k] = k
#	#	writer.writerow(key_row)
#	#	for row in data:
#	#		writer.writerow(row)