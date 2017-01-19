# coding: utf-8

import sys
import re
import regex as re

import platform

import codecs

import ScoringClass
from ScoringClass import ScoringClass
import DifficultyEstimationClass
from DifficultyEstimationClass import DifficultyEstimationClass

import chardet

import unicodedata

from operator import add


# Change default character encoding
reload(sys)                         #Reload module
sys.setdefaultencoding('utf-8')     #Set character encoding to 'utf-8'

class MainClass:
	"""message"""

	# config number (ninimum sentence in secsion)
	minLineNumber = 1

	def __init__(self):
		MainClass.sc = ScoringClass()

	def readfile(self,imputfilename):
		"""read imput file from imputfilename(file) to rawText"""
		with open(imputfilename,mode="r") as file:
			encode = chardet.detect(file.read())[u"encoding"]
		try:
			self.rawText = Text(codecs.open(imputfilename,"r",encoding=encode).read().decode(encode))
		except UnicodeDecodeError:
			sys.exit("error! codecs is not supported.")

	def splitSection(self):
		"""split rawFile to sectionList and sentenceList"""
		# split rawFile by "\n" and set to sectionList 
		self.sectionList = [Text(t) for t in self.rawText.text.split(u"\r\n" or u"\n" or u"\r")]

	def splitSentence(self):
		# split foreach sectionList[] to sentenceList by "。\.．"
		pre = re.compile(ur"[。]")
		for section in self.sectionList[:]:
			section.sentenceList = [Text(t) for t in pre.split(section.text) if len(t) > 0]

	def writefile(self,outputfilename):
		with codecs.open(outputfilename,"w",encoding="utf-8-sig") as file:
			for section in main.defficultySortedSectionList:
				file.write((unicode(main.sectionList.index(section)) + section.text + u"\n:diff=" +unicode(section.difficulty) + u",score="+unicode(section.score) +u"\n").encode("utf-8-sig"))
				keylist = reduce(add,section.keywords)
				for match in keylist:
					file.write("\t" + match + ":" + str(ScoringClass.clueword[match] if match in ScoringClass.clueword else ScoringClass.keysentence[match]))
					file.write("\n")

	def scoringSentence(self):
		for section in [sec for sec in self.defficultySortedSectionList]:
			if len(section.sentenceList)>=MainClass.minLineNumber:
				section.keywords = MainClass.sc.scoreSentenceList([sea.text for sea in section.sentenceList])
			else:
				section.keywords = [[]]

	def scoringSection(self):
		for section in self.sectionList:
			section.score = sum([MainClass.sc.clueword.get(key) or MainClass.sc.keysentence.get(key) for key in reduce(add,section.keywords)])
			#if hasattr(section,u"keywords"):
			#	keylist = reduce(add,section.keywords)
			#	section.score = sum([MainClass.sc.clueword.get(key) or MainClass.sc.keysentence.get(key) for key in reduce(add,section.keywords)])

	def sort(self):
		self.defficultySortedSectionList = sorted(self.sectionList,key=lambda section:section.difficulty,reverse=True)

class Text:
	def __init__(self,text):
		self.text = unicode(text)

if __name__ == "__main__":
	print "start main class as main"
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
		a = lambda x:max(x) if len(x) > 0 else 0
		b = lambda x:sum(x)/len(x) if len(x) > 0 else 0
		section.difficulty = a(section.difficultyList)
	
	main.sort()

    # Scoring to section
	main.scoringSentence()

	main.scoringSection()

    # write file 
	main.writefile(outputfilename)