# Difficulty Estimation Kaneko
# encoding: utf-8
# import MeCab

import sys
import csv

import chardet
from chardet.universaldetector import UniversalDetector

import codecs

import regex as re

class DifficultyEstimationClass:

    difficultyNormal = 1

    fcorpus = []
    keyword = {}
    
    hitcount = 0
    difficulty = []

    word = [ ]

    def openInputFile(self, filename='./input.txt'):
        # Open input file
        self.fin = open(filename,'r')

    def closeInputFile(self):
         #Close input file
        self.fin.close()

    def openCorpusFile(self):
        # Open corpus file
        for i in range(1,13):
            self.fcorpus.append(open('./corpus/kanji_level'+str(i)+'.csv',"rb"))
        self.fcorpus.append(open('./corpus/alpha.txt',"rb"))
        #self.fcorpus.append(open('./corpus/hira.txt',"rb"))
        #self.fcorpus.append(open('./corpus/hkata.txt',"rb"))
        #self.fcorpus.append(open('./corpus/kata.txt',"rb"))
        self.fcorpus.append(open('./corpus/symbol.txt',"rb"))

    def closeCorpusFile(self):
        # Close corpus files
        for fi in self.fcorpus:
            fi.close()

    def openOutputFile(self, filename='./output.txt'):
        # Open output file
        self.fout = open('./result.txt','w')

    def closeOutputFile(self):
        # Close output file
        self.fout.close()

    def makeDictionary(self):

        # sysモジュールをリロードする
        reload(sys)
        # デフォルトの文字コードを変更する．
        sys.setdefaultencoding('utf-8')

        self.openCorpusFile()

        # Set corpus character and difficulty to keyword
        for fc in self.fcorpus:
            detector = UniversalDetector()
            try:
                while True:
                    bynary = fc.readline()
                    if bynary == b"":#read to end
                        break
                    detector.feed(bynary)
                    if detector.done:
                        break
            finally:
                detector.close()

            codec = detector.result
            fc.seek(0)
            reader = csv.reader(fc)
            header = reader.next()
            if codec.get("encoding") == None:
                codec["encoding"] = "shift-jis"######  Z  U  R  U  I  !
            for row in reader:
                try:
                    DifficultyEstimationClass.keyword[row[0].decode(codec.get("encoding"))] = int(row[1].decode(codec.get("encoding")))
                except UnicodeDecodeError:
                    exit("error!")
        self.closeCorpusFile()
        
    def estimateDifficulty(self,sentence):
        difficulty = 0.0
        count = 0
        # all alphabet (include "hiragana,katakana,kanji")
        chars = re.findall(ur"[\p{Alphabetic}]",sentence)
        # Start Checking

        #matching hiragana and katakana
        reHiraKata = re.compile(ur"[\p{Hiragana}\p{Katakana]")
        #matching kanji
        reHan = re.compile(ur"[\p{Han}]")
        for char in chars:
            if reHiraKata.match(char):
                difficulty += DifficultyEstimationClass.difficultyNormal
            elif reHan.match(char):
                #if not memoried kanji, it's difficulty is 12
                difficulty += DifficultyEstimationClass.keyword.get(char,12)
        #null string has no difficulty
        return difficulty/len(chars) if len(chars) != 0 else 0
    

    def open(self):
        self.openInputFile()
        self.openCorpusFile()
        self.openOutputFile()

    def close(self):
        self.closeInputFile()
        self.closeCorpusFile()
        self.closeOutputFile()

if __name__ == "__main__":
    print "start DifficultyEstimation"
    this = DifficultyEstimationClass()
    this.open()
    this.makeDictionary()
    with codecs.open("input_main.txt",mode="r",encoding="utf-8-sig") as file:
        texts = file.readlines()
    with codecs.open("output_estimate.txt",mode="w",encoding="utf-8-sig") as file:
        for i,text in enumerate(texts):
            if i != 0:
                file.write(u"\r\n")
            file.write(text)
            if not text.endswith(u"\n"):
                file.write("\n")
            file.write(u"difficluty = "+unicode(this.estimateDifficulty(text)))
    this.close()
    print "THE END"