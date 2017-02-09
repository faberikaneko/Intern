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
    if clueword == None:
        scorere = re.compile(ur"(?<key>.*?) : \[ (?<image>\d+\.\d+) (?<table>\d+\.\d+) (?<graph>\d+\.\d+) (?<flow>\d+\.\d+)\]",
                                flag=re.UNICODE)
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
                clueword[word] = imagescore
    return

def openClueWordDB(
        dbName=u"WordDB.sqlite3",
        tableName=u"wordscore",
        filename=u"output2_all (3).txt"
    ):
    '''<- dbname : filename to read
<- tableName : tablename to read/write
read clueword table in Database into dict(clueword)
if no table or dbfile, read textfile and save it'''
    global clueword
    if clueword == None:
        try:
            conn = sqlite3.connect(dbName)
            with conn:
                cr = conn.cursor()
                if cr.execute(u"select count(*) from sqlite_master where type=\"table\" and name=?;",(tableName,)).fetchone()[0] == 0:
                    message = u"create table "+tableName+u"\n (word ntext,image real,tables real,graph real,flow real);"
                    cr.execute(message)
                    openClueWord(filename)
                    message = u"insert into "+tableName+" values (:key,:image,:table,:graph,:flow)"
                    for item in clueword.items():
                        args = (item[0],item[1][u"image"],item[1][u"table"],item[1][u"graph"],item[1][u"flow"])
                        cr.execute(message,args)
                else :
                    clueword = {}
                    message = u"select * from "+tableName
                    for row in cr.execute(message):
                        word = row[0]
                        dic = {u"image":row[1],u"table":row[2],u"graph":row[3],u"flow":row[4]}
                        clueword[row[0]] = ImageScore(dic)
        except sqlite3.Error as e:
            print e.message
            raise
        except Exception as e:
            print e.message
            raise

#read text
def scoreSentenceByWord(text):
    """ in > text (one sentence)
        out> matching word list[]"""
    matching = []
    #searching word
    for item in clueword.items():
        if text in item[0]:
            matching.append(item)
    return matching

openClueWordDB(u"WordDB.sqlite3",filename="scoreimage.txt")

#てすとプログラム
if __name__ == "__main__":
    pass