# -*- coding:utf-8 -*-

import MeCab
import sys
import codecs
import csv

class ScoringClass:
	"""scoring sentense"""
	clueword = None
	keysentence = None

	def openClueWord(self,filename="ClueWord_List.csv"):
		if ScoringClass.clueword == None:
			ScoringClass.clueword = {}
			# read database(ClueWord)->data
			with open(filename,"rt") as f:
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
					ScoringClass.keysentence[row[0].replace("～","*").decode("utf-8")] = int(row[2].decode("utf-8"))
		return

	#分割する文章を読み込む
	def scoreSentence(self,text):
		point = 0
		m = MeCab.Tagger("-Owakati")
		node = m.parseToNode(text.encode("utf-8"))
		ans = ""
		node = node.next
		while node.next:
			word = (node.surface.decode("utf-8"),node.feature.decode("utf-8"))
			ans += "%s %s\n"%word
			if word[0] in ScoringClass.clueword.keys():
				point += ScoringClass.clueword[word[0]]
#				print"%s %d"%(node.surface.decode("utf-8"),ScoringClass.clueword[word[0]])
			node = node.next
		print point
		return point

	def scoreSentenceList(self,textList):
		scoreList = []
		for text in textList:
			score = self.scoreSentence(text)
			scoreList.append((text,score))
		return scoreList

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
	with open(filename,"rt") as file:
		textList = file.readlines()
	scores = this.scoreSentenceList(map(lambda t : t.replace("\n","").decode("utf-8") , textList))
	filename = "output_scorig.txt"
	with open(filename,"wt") as f:
		for score in scores:
			f.write(score[0] + ":" + str(score[1]) + "\n")
	

	#print(key)

	#with open("Output.csv","wb") as f:
	#	writer = csv.DictWriter(f,key)
	#	key_row = {}
	#	for k in key:
	#		key_row[k] = k
	#	writer.writerow(key_row)
	#	for row in data:
	#		writer.writerow(row)