# coding: utf-8

import sys
import re

class MainClass:
	"""message"""

	def __init__(self,filename,outputname):
		# デフォルトの文字コードを変更する．
		reload(sys)
		sys.setdefaultencoding('utf-8')

		self.textList = []
		with open(filename,"rt") as f:
			self.textList = map(lambda t:t.decode("utf-8"),f.readlines())
		self.sectionList = []
		pre = re.compile(ur'[。\.\n]')
		for text in self.textList:
			self.sectionList.append(filter(lambda t:len(t) > 0,pre.split(text)))
		print 'defaultencoding:', sys.getdefaultencoding()
		with open(outputname,"wt") as f:
			for line in self.sectionList:
				for text in line:
					f.write(text.encode("utf-8")+"\n")
				f.write("yes\n" if len(line)>2 else "no\n")
		return

if __name__ == "__main__":
	print "start main class"
	filename = "input_main.txt"
	outputname = "output_main.txt"
	main = MainClass(filename,outputname)

