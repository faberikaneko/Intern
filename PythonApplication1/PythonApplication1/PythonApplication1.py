# -*- coding:utf-8 -*-

import MeCab
import sys
import codecs

m = MeCab.Tagger("-Owakati")

import csv
##document
class ScoringClass:
	"""scoring sentense"""

	def openClueWord(self,filename="ClueWord_List.csv"):
		# データベースを読み込む(ClueWord)->data
		self.clueword = {}
		with open(filename,"rb") as f:
			reader = csv.reader(f)
			#ヘッダ行の読み飛ばし
			next(reader)
			#dataの表現部分：重み辞書を作成
			for row in reader:
				self.clueword[row[0]] = int(row[2])
		return

	def openSentenceExpression(self,filename="SentenceExpression_List.csv"):
		#データベース読み込む(SentenceExpression)->dataC
		dataC = []
		with open(filename,"rb") as f:
			reader = csv.reader(f)
			next(reader)
			self.keysentence = {}
			#dataCの表現部分：重み辞書を作成
			for row in reader:
				self.keysentence[row[0].replace("~","")] = int(row[2])
		return

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
		self.oepnClueWord()
		self.openSentenceExpression()

#てすとプログラム
if __name__ == "__main__":
	print "Start ScorinClass"
	this = ScoringClass()
	score = this.scoringSentence("のし袋の使用量は３年間に１５％減少している。")
		

	#print(key)

	#with open("Output.csv","wb") as f:
	#	writer = csv.DictWriter(f,key)
	#	key_row = {}
	#	for k in key:
	#		key_row[k] = k
	#	writer.writerow(key_row)
	#	for row in data:
	#		writer.writerow(row)