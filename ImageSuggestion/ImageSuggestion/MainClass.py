# coding: utf-8

import sys
import re

import codecs

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
		"""read imput file from imputfilename(file) to rawText"""
		try:
			self.rawText = Text(codecs.open(imputfilename,"r",encoding="utf-8-sig").read().decode("utf-8"))
		except UnicodeDecodeError:
			try:
				self.rawText = Text(codecs.open(imputfilename,"r",encoding="shift-jis").read().deoced("shift-jis"))
			except UnicodeDecodeError:
				sys.exit("error! codecs is not supported.")

	def splitSection(self):
		"""split rawFile to sectionList and sentenceList"""
		# split rawFile by "\n" and set to sectionList 
		self.sectionList = [Text(t) for t in self.rawText.text.split(u"\r\n" or u"\n" or u"\r")]

	def splitSentence(self):
		# split foreach sectionList[] to sentenceList by "。\.．"
		pre = re.compile(ur'[。\.．]')
		self.sentenceList = [[]]
		for section in self.sectionList:
			section.sentenceList = filter(lambda t:len(t.text) > 0,[Text(t) for t in pre.split(section.text)])

	def writefile(self,outputfilename):
		None

	def do(self):
		sc = ScoringClass
		scores = []
		for section in filter(lambda s : len(s) > MainClass.minLineNumber,self.sectionList):
			scores.append(sc.scoreSentenceList(section))
		return scores

class Text:
	def __init__(self,text):
		self.text = unicode(text)

if __name__ == "__main__":
	print "start main class"
	imputfilename = "input_main.txt"
	outputfilename = "output_main.txt"

    # Initialize MainClass and make sectionList
	main = MainClass()
	main.readfile(imputfilename)
	main.splitSection()
	main.splitSentence()

    # TODO: Difficulty Estimation

	dec = DifficultyEstimationClass()
	dec.makeDictionary()
	for section in main.sectionList[:]:
		section.difficultyList = [dec.estimateDifficulty(s.text) for s in section.sentenceList]
		a = lambda x:max(x)
		b = lambda x:sum(x)/len(x) if len(x) > 0 else 0
		section.difficulty = a(section.difficultyList)

	difsortedSectionList = sorted(main.sectionList,key=lambda section:section.difficulty,reverse=True)
	print [section.text.encode("utf-8") for section in main.sectionList]

		

    # Scoring to section
	#scores = main.do()

    # 
	with codecs.open(outputfilename,"w",encoding="utf-8-sig") as file:
		for section in main.sectionList[:]:
			file.write((section.text + ":" +str(section.difficulty) +u"\n").encode("utf-8-sig"))