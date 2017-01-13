# -*- encode:utf-8 -*-

import sys
import re

class MainClass:
	"""message"""

	def __init__(self,filename,outputname):
		self.textList = []
		with open(filename,"rt") as f:
			self.textList = f.readlines()
		self.sectionList = []
#		pre = re.compile(r'[.。]')
		for text in self.textList:
#			self.sectionList.append(pre.split(text))
			self.sectionList.append(text.split("。"))
		with open(outputname,"wt") as f:
			for line in self.sectionList:
				for text in line:
					f.write(text)
		self.sectionList
		return

if __name__ == "__main__":
	print "start main class"
	filename = "input_main.txt"
	outputname = "output_main.txt"
	main = MainClass(filename,outputname)

