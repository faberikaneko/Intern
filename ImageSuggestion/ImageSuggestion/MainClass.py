# coding: utf-8

import sys
import re

import ScoringClass
import DifficultyEstimationClass

class MainClass:
	"""message"""

	def __init__(self,imputfile,outputfile):
		# Change default character encoding
		reload(sys)                                        #Reload module
		sys.setdefaultencoding('utf-8')     #Set character encoding to 'utf-8'

        # Set sentences to textList from inputfile
		self.textList = []
		with open(imputfile,"rt") as file:
            # Set sentences encoded 'utf-8' from input file to textList
			self.textList = map(lambda t:t.decode("utf-8"),file.readlines())
        
        # Split by '。', '\.', '\n' sentences and set to sectionList from textList
		self.sectionList = []
		pre = re.compile(ur'[。\.\n]')
		for text in self.textList:
			self.sectionList.append(filter(lambda t:len(t) > 0,pre.split(text)))
		return


	def do(self):
		sc = ScoringClass
		scores = []
		for section in filter(lambda s : len(s) > 3,self.sectionList):
			print "yes"
			scores.append(this.scoreSentenceList(section))
		return scores

if __name__ == "__main__":
	print "start main class"
	imputfile = "input_main.txt"
	outputfile = "output_main.txt"

    # Initialize MainClass and make sectionList
	main = MainClass(imputfile,outputfile)

    # TODO: Difficulty Estimation

    # Scoring to section
	scores = main.do()

    # 
	with open(outputfile,"wt") as f:
		for line in main.sectionList:
			for text in line:
				f.write(text.encode("utf-8")+"\n")
			f.write("yes\n" if len(line)>2 else "no\n")