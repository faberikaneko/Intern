# -*- coding:utf-8 -*-

import sys
import codecs
import sqlite3

from multiprocessing import Lock

wlock = Lock()
glock = Lock()

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
                if word.startswith(u"～"):
                    word = word[1:]
                if word.endswith(u"～"):
                    word = word[:-1]
                word = re.sub(u"～",u"(?:.*?)",word)
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
            #for key in clueword:
            #    for tag in ImageScore.taglist:
            #        clueword[key].dict[tag]/=filecount 
            asd = dict.fromkeys(ImageScore.taglist,0.0)
            for value in clueword.values():
                for tag in ImageScore.taglist:
                    asd[tag] += value[tag]
        return clueword

    @classmethod
    def _make_regulers(cls):
        if cls._clueword == None:
            cls.get_clueword()
        cls._regulers = []
        for key in cls._clueword:
            word = re.sub(u"～",u"(?:.*?)",key)
            cls._regulers.append((re.compile(word),key))

    @classmethod
    def get_clueword(cls):
        with wlock:
            if cls._clueword == None:
                cls._clueword = cls._opendict_bylist(u"dictlist.txt")
        return cls._clueword
    @classmethod
    def get_regs(cls):
        with glock:
            if cls._regulers == None:
                cls._make_regulers()
        return cls._regulers

#てすとプログラム
if __name__ == "__main__":
    pass