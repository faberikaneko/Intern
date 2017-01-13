# -*- coding:utf-8 -*-

import MeCab
import sys
import codecs

m = MeCab.Tagger("-Owakati")

import csv
##document
class ScoringClass:
	"""scoring sentense"""

	key = ['\xef\xbb\xbfkeyword', 'type', 'importance', 'list1', 'list3', 'list2']

	def readClueWord(self,filename="ClueWord_List.csv"):
		# データベースを読み込む(ClueWord)->data
		data = []
		with open(filename,"rb") as f:
			reader = csv.DictReader(f)
			for row in reader:
				data.append(row)
		#dataの表現部分：重み辞書を作成
		self.clueword = {}
		for d in data:
			self.clueword[d[ScoringClass.key[0]]] = int(d[ScoringClass.key[2]])
		return

	def readSentenceExpression(self,filename="SentenceExpression_List.csv"):
		#データベース読み込む(SentenceExpression)->dataC
		dataC = []
		with open(filename,"rb") as f:
			reader = csv.DictReader(f)
			for row in reader:
				dataC.append(row)
		#dataCの表現部分：重み辞書を作成
		self.keysentence = {}
		for d in dataC:
			self.keysentence[d[ScoringClass.key[0]].replace("~","")] = int(d[ScoringClass.key[2]])

	#分割する文章を読み込む
	def scoringSentence(self,text):
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

	def __init__(self):
		self.readClueWord()
		self.readSentenceExpression()

#てすとプログラム
if __name__ == "__main__":
	print "start main"
	this = ScoringClass()
	this.scoringSentence("のし袋の使用量は３年間に１５％減少している。")
		

	#print(key)

	#with open("Output.csv","wb") as f:
	#	writer = csv.DictWriter(f,key)
	#	key_row = {}
	#	for k in key:
	#		key_row[k] = k
	#	writer.writerow(key_row)
	#	for row in data:
	#		writer.writerow(row)