# Difficulty Estimation Kaneko
# coding: utf-8
# import MeCab

import sys
import csv

class DifficultyEstimationClass:

	fcorpus = []
	keyword = {}
	
	hitcount = 0
	difficulty = []

	word = [ ]

	def openInputFile(self, filename='./input.txt'):
		# Open input file
		self.fin = open(filename,'r')

	def closeInputFile(self):
		 #Close input file
		self.fin.close()

	def openCorpusFile(self):
		# Open corpus file
		for i in range(1,13):
			self.fcorpus.append(open('./corpus/kanji_level'+str(i)+'.csv',"r"))
		self.fcorpus.append(open('./corpus/alpha.txt',"r"))
		self.fcorpus.append(open('./corpus/hira.txt',"r"))
		self.fcorpus.append(open('./corpus/hkata.txt',"r"))
		self.fcorpus.append(open('./corpus/kata.txt',"r"))
		self.fcorpus.append(open('./corpus/symbol.txt',"r"))

	def closeCorpusFile(self):
		# Close corpus files
		for fi in self.fcorpus:
			fi.close()

	def openOutputFile(self, filename='./output.txt'):
		# Open output file
		self.fout = open('./result.txt','w')

	def closeOutputFile(self):
		# Close output file
		self.fout.close()

	def makeDictionary(self):

		# sysモジュールをリロードする
		reload(sys)
		# デフォルトの文字コードを変更する．
		sys.setdefaultencoding('utf-8')

		self.openCorpusFile()

		# Set corpus character and difficulty to keyword
		for fc in self.fcorpus:
			reader = csv.reader(fc)
			codec = "utf-8"
			reader.next()
			for row in reader:
				try:
					DifficultyEstimationClass.keyword[row[0].decode(codec)] = int(row[1].decode(codec))
				except UnicodeDecodeError:
					codec = "shift-jis"
					DifficultyEstimationClass.keyword[row[0].decode(codec)] = int(row[1].decode(codec))
		self.closeCorpusFile()
		
	def estimateDifficulty(self,sentence):
		difficulty = 0.0
		count = 0
		chars = filter(lambda t:t != "",list(sentence))
		# Start Checking

		for char in chars:
			if char in DifficultyEstimationClass.keyword.keys():
				difficulty += DifficultyEstimationClass.keyword[char]
				count += 1
#				print char + ":" + str(DifficultyEstimationClass.keyword[char])
			else :
				difficulty += 1
				count += 1
#		print str(difficulty) + "/" + str(count)
		return difficulty/count if count != 0 else 0
	

	def open(self):
		self.openInputFile()
		self.openCorpusFile()
		self.openOutputFile()

	def close(self):
		self.closeInputFile()
		self.closeCorpusFile()
		self.closeOutputFile()




"""
if __name__ == "__main__":
	print "start DifficultyEstimation"
	this = DifficultyEstimation()
	this.open()
	this.makeDictionary()
	this.splitSentences()
	this.close()
	print "THE END"
	"""
	