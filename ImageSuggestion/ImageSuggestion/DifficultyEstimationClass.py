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
		# デフォルトの文字コードを出力する．
		print 'defaultencoding:', sys.getdefaultencoding()

		# Set corpus character and difficulty to keyword
		for fc in self.fcorpus:
			reader = csv.reader(fc)
			codec = "utf-8"
			for row in reader:
				try:
					DifficultyEstimationClass.keyword[row[0].decode(codec)] = row[1].decode(codec)
				except UnicodeDecodeError:
					codec = "shift-jis"
					DifficultyEstimationClass.keyword[row[0].decode(codec)] = row[1].decode(codec)
#			print row[0] + " : " + self.keyword[count][row[0]]
		print "END MAKING DICTIONARY"
		
#		# Test
#		samplechar = "一"
#		sam = samplechar.decode('utf-8')
#		count = 0
#		for i in self.keyword:
##			print self.keyword[count].keys()
#			for s in self.keyword[count].keys():
#				print isinstance(samplechar,str)
#				print s + "  " + samplechar
#				if s==samplechar:
#					print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
##				print "HIT"
#			count += 1

	def splitSentences(self,sentence):
		# Split sentences to character
		self.word = [ ]
		for char in sentence:
			word.append(char)
			word
	
	def estimateDifficulty(self):
		# Start Checking
		print "CHECK"

		for w in word:
			for fc in fcorpus:
		#		print i
				reader = csv.reader(fc)
		#		header = next(reader)
				for row in reader:
		#			print row[0]
		#			print w
					if w==row[0]:
						hitcount+=1
						difficulty.append(row[2])
						print "HIT"
			print "END CORPUS"
		print "END SENTENCE"
	

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
	