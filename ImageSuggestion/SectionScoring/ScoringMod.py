# -*- coding:utf-8 -*-

import sys
import codecs
import sqlite3

from multiprocessing import Lock

wlock = Lock()

from imagescore import ImageScore

#External import package to check Unicode parameter
import regex as re
class ScoringClass:
    _clueword = None
    _regulers = None

    @staticmethod
    def _openClueWord(filename):
        ''' <- filename : filename to read default = scoreimage.txt
            -> clueword:dict{word:unicode,score:ImageScore}'''
        scorere = re.compile(
            ur"(?<key>.*?) : \[ (?<image>\d+\.\d+) (?<table>\d+\.\d+) (?<graph>\d+\.\d+) (?<flow>\d+\.\d+)\]",
            flag=re.UNICODE
        )
        clueword = {}
        a = 0.0
        # read database(ClueWord)->data
        with codecs.open(filename,"r","utf-8-sig") as file:
            #make data word:importance dict
            for line in file.readlines():
                scoreobj = scorere.search(line)
                word = scoreobj.group(u"key")
                score = dict()
                for tag in ImageScore.taglist:
                    score[tag] = float(scoreobj.group(tag))
                clueword[word] = ImageScore(score)
        return clueword
    
    @staticmethod
    def _opendict_bylist(dictlistfilename):
        clueword = {}
        with codecs.open(dictlistfilename,
                            mode=u"r",
                            encoding=u"utf-8-sig"
        ) as file:
            dictnames = file.read().strip().split()
            for dictname in dictnames:
                subdict = ScoringClass._openClueWord(dictname)
                for key in subdict:
                    if key in clueword:
                        clueword[key] += subdict[key]
                    else:
                        clueword[key] = subdict[key]
            filecount = len(dictnames)
            for key in clueword:
                for tag in ImageScore.taglist:
                    clueword[key].dict[tag]/=filecount
        return clueword

    @classmethod
    def get_clueword(cls):
        if cls._clueword == None:
            with wlock:
                if cls._clueword == None:
                    cls._clueword = cls._opendict_bylist(u"dictlist.txt")
        return cls._clueword

#てすとプログラム
if __name__ == "__main__":
    d = ScoringClass.get_clueword()
    with codecs.open("dictdata.txt","w",encoding='utf-8-sig') as file:
        file.write(u'{\n\t')
        for i,item in enumerate(d.items()):
            if i != 0:
                file.write(u'\n\t')
            file.write(u'u\''+item[0]+u'\':[')
            for j,tag in enumerate(ImageScore.taglist):
                if j != 0:
                    file.write(u',')
                file.write(unicode(item[1][tag]))
            file.write(u'],')
        file.write(u'\n}')

    with codecs.open('dictdata.txt','r',encoding='utf-8-sig') as file:
        dd = eval(file.read())
        a = [0.,0.,0.,0.]
        for val in dd.values():
            for i in range(4):
                a[i] += val[i]
        print(a)