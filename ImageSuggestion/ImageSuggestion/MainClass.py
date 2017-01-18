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
			ans = codecs.open(imputfilename,"r",encoding="utf-8-sig").read().decode("utf-8")
		except UnicodeDecodeError:
			ans = codecs.open(imputfilename,"r",encoding="shift-jis").read().deoced("shift-jis")
		return ans

	def split(self):
		"""rawFile to sectionList and sentenceList"""
		# split rawFile by "\n" and set to sectionList 
		self.sectionList = filter(lambda t:len(t) > 0,map(lambda t:t.replace(u"\r\n" or u"\n" or u"\r" ,u""),self.rawText.split(u"\r\n" or u"\n" or u"\r")))
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
			scores.append(sc.scoreSentenceList(section))
		return scores

if __name__ == "__main__":
	print "start main class"
	imputfilename = "input_main.txt"
	outputfilename = "output_main.txt"

    # Initialize MainClass and make sectionList
	main = MainClass()
	main.rawText = main.readfile(imputfilename)
	main.split()

    # TODO: Difficulty Estimation

	dec = DifficultyEstimationClass()
	dec.makeDictionary()
	difficultySectionDict = {}
	for section in main.sectionList:
		difList = [dec.estimateDifficulty(s) for s in main.sentenceList[main.sectionList.index(section)]]
		difficultySectionDict[section] = sum(difList)/len(difList)

    # Scoring to section
	#scores = main.do()

    # 
	with codecs.open(outputfilename,"w",encoding="utf-8-sig") as file:
		for line in main.sectionList:
			file.write((line + ":" +str(difficultySectionDict[line]) +u"\n").encode("utf-8-sig"))