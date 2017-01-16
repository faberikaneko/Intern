# coding: utf-8

import sys
import re

import ScoringClass
import DifficultyEstimationClass
from DifficultyEstimationClass import DifficultyEstimationClass

class MainClass:
	"""message"""

	minLineNumber = 1

	def __init__(self):
		# Change default character encoding
		reload(sys)                                        #Reload module
		sys.setdefaultencoding('utf-8')     #Set character encoding to 'utf-8'

		return

	def readfile(self,imputfilename):
		"""read imput file from imputfilename(file) to rawFile and sectionList and sentenceList"""
		with open(imputfilename,"rt") as file:
			# Set sentences encoded 'utf-8' from input file to textList
			try:
				self.rawFile = file.read().decode("utf-8")
			except UnicodeDecodeError:
				self.rawFile = file.read().decode("shift-jis")
			# split rawFile to sectionList[] by "\n" 
			self.sectionList = filter(lambda t:len(t) > 0,map(lambda t:t.replace(u"\n",u""),self.rawFile.split(u"\n")))
			# split foreach sectionList[] to sentenceList by "。\.．"
			self.sentenceList = []
			pre = re.compile(ur'[。\.．]')
			for sentence in self.sectionList:
				self.sentenceList.append(filter(lambda t:len(t) > 0,pre.split(sentence)))

	def writefile(self,outputfilename):
		None

	def do(self):
		sc = ScoringClass
		scores = []
		for section in filter(lambda s : len(s) > MainClass.minLineNumber,self.sectionList):
			print "yes"
			scores.append(sc.scoreSentenceList(section))
		return scores

if __name__ == "__main__":
	print "start main class"
	imputfilename = "input_main.txt"
	outputfilename = "output_main.txt"

    # Initialize MainClass and make sectionList
	main = MainClass()
	main.readfile(imputfilename)

    # TODO: Difficulty Estimation

	dec = DifficultyEstimationClass()
	dec.openCorpusFile()
	dec.makeDictionary()
	sentenceDifficultyDict = dec

	print main.sentenceList
    # Scoring to section
	scores = main.do()

    # 
	with open(outputfile,"wt") as file:
		for line in main.sectionList:
			for text in line:
				file.write(text.encode("utf-8")+"\n")
			file.write("yes\n" if len(line)>2 else "no\n")