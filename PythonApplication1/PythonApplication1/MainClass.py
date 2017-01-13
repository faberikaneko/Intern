# -*- encode:utf-8 -*-

import sys

class MainClass:
	"""message"""

	def __init__(self,filename):
		self.textList = []
		with open(filename,"rt") as f:
			self.textList = f.readlines()
		return

if __name__ == "__main__":
	print "start main class"
	filename = "input_main.txt"
	main = MainClass(filename)

