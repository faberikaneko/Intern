# -*- coding:utf-8 -*-

import sys
import codecs
import sqlite3

from imagescore import ImageScore

#External import package to check Unicode parameter
import regex as re

#External import package to check encoding of file
import chardet
from chardet.universaldetector import UniversalDetector

#dict[key:unicode] -> (dict[typename:unicode] -> score:float)
clueword = None

def openClueWord(filename):
    ''' <- filename : filename to read default = scoreimage.txt
        -> No return
        read scoreimage.txt into dict(clueword)'''
    global clueword
    scorere = re.compile(
        ur"(?<key>.*?) : \[ (?<image>\d+\.\d+) (?<table>\d+\.\d+) (?<graph>\d+\.\d+) (?<flow>\d+\.\d+)\]",
        flag=re.UNICODE
    )
    if clueword == None:
        clueword = {}

    # read database(ClueWord)->data
    with codecs.open(filename,"r","utf-8-sig") as file:
        #make data word:importance dict
        for line in file.readlines():
            scoreobj = scorere.search(line)
            word = scoreobj.group(u"key")
            score = dict()
            for tag in ImageScore.taglist:
                score[tag] = float(scoreobj.group(tag))
            imagescore = ImageScore(score)
            if word in clueword:
                oldscore = clueword[word]
                imagescore += oldscore
            clueword[word] = imagescore
    return

def opendict_bylist(dictlistfilename):
    if clueword == None:
        with codecs.open(dictlistfilename,
                         mode=u"r",
                         encoding=u"utf-8-sig"
        ) as file:
            dictnames = file.read().strip().split()
            for dictname in dictnames:
                openClueWord(dictname)
            filecount = len(dictnames)
            for key in clueword:
                for tag in ImageScore.taglist:
                    clueword[key][tag] / filecount

opendict_bylist(u"dictlist.txt")

#てすとプログラム
if __name__ == "__main__":
    pass