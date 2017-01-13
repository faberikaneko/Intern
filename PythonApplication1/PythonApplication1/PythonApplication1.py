# -*- coding:utf-8 -*-

import MeCab
import sys
import codecs

m = MeCab.Tagger("-Owakati")

import csv
##document
class ScoringClass:
	"""scoring sentense"""
	clueword = None
	keysentence = None

	def openClueWord(self,filename="ClueWord_List.csv"):
		if ScoringClass.clueword == None:
			ScoringClass.clueword = {}
			# データベースを読み込む(ClueWord)->data
			with open(filename,"rb") as f:
				reader = csv.reader(f)
				#ヘッダ行の読み飛ばし
				next(reader)
				#dataの表現部分：重み辞書を作成
				for row in reader:
					ScoringClass.clueword[row[0]] = int(row[2])
		return

	def openSentenceExpression(self,filename="SentenceExpression_List.csv"):
		if ScoringClass.keysentence == None:
			ScoringClass.keysentence = {}
			#データベース読み込む(SentenceExpression)->dataC
			with open(filename,"rb") as f:
				reader = csv.reader(f)
				next(reader)
				#dataCの表現部分：重み辞書を作成
				for row in reader:
					ScoringClass.keysentence[row[0].replace("~","")] = int(row[2])
		return

	#分割する文章を読み込む
	def scoreSentence(self,text):
		point = 0
		m = MeCab.Tagger("-Owakati")
		node = m.parseToNode(text)
		ans = ""
		while node:
			ans += "%s %s\n"%(node.surface,node.feature)
			if node.surface in self.clueword.keys():
				point += self.clueword[node.surface]
				print"%s %d"%(node.surface.decode("utf-8"),self.clueword[node.surface])
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
		self.openClueWord()
		self.openSentenceExpression()

#てすとプログラム
if __name__ == "__main__":
	print "Start ScorinClass"
	this = ScoringClass()
	textList = []
	filename = "text.txt"
	with open(filename,"rt") as f:
		textList = f.read().split("\n")
	scores = this.scoreSentenceList(textList)
	filename = "output.txt"
	with open(filename,"wt") as f:
		for score in scores:
			f.write(score[0])
			f.write(str(score[1]))
	

	#print(key)

	#with open("Output.csv","wb") as f:
	#	writer = csv.DictWriter(f,key)
	#	key_row = {}
	#	for k in key:
	#		key_row[k] = k
	#	writer.writerow(key_row)
	#	for row in data:
	#		writer.writerow(row)