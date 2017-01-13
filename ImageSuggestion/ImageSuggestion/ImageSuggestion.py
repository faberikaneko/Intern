# Difficulty Estimation Kaneko
# coding: utf-8
# import MeCab

import sys
import csv
import codecs
import itertools

class DifficultyEstimation:

    fcorpus = [ ]
    keyword = [ { } ]
    
    hitcount = 0
    difficulty = [ ]

    word = [ ]

    def openInputFile(self, filename='./input.txt'):
        # Open input file
        self.fin = open(filename,'rb')

    def closeInputFile(self):
         #Close input file
        self.fin.close()

    def openCorpusFile(self):
        # Open corpus file
        for i in range(1,13):
            self.fcorpus.append(open('./corpus/kanji_level'+str(i)+'.csv',"rb"))

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
        # デフォルトの文字コードを出力する．
        print 'defaultencoding:', sys.getdefaultencoding()

        # Set corpus character and difficulty to keyword
        count = 0
        for fc in self.fcorpus:
            reader = csv.reader(fc)
            next(reader)
            codec = "utf-8"
            leveldict = {}
            for row in reader:
                try:
                    row[0].decode(codec)
                except UnicodeDecodeError:
                    codec = "shift-jis"
                leveldict[row[0].decode(codec)] = row[1]
            self.keyword.append(leveldict)
#        print "END MAKING DICTIONARY"
        
#        # Test
#        samplechar = "一"
#        sam = samplechar.decode('utf-8')
#        count = 0
#        for i in self.keyword:
#            for s in i.keys():
##                print s + "  " + samplechar
#                if s==sam:
#                    print "Hit:" + s + str(i[s])
#                    count += 1

    def splitSentences(self,textList):
        # Split sentences to character
        self.word = [ ]
        for line in textList:
            for i in list(line):
                self.word.append(i)#.encode('utf-8'))
    
    def estimateDifficulty(self):
        # Start Checking
        print "CHECK"

        count = 0
        score = 0
        for w in self.word:
            scorein = 0
            for i in self.keyword:
                for s in i.keys():
                    if w==s:
                        scorein = int(i[s])
            
            score += scorein if scorein!=0 else 0.1
            print w.encode("shift-jis") + ":" + str(scorein if scorein != 0 else 0.1)
            count += 1
        print "END SENTENCE"
        return float(score)/count
    

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
    this = DifficultyEstimation()
    this.open()
    this.makeDictionary()
    this.splitSentences("墾田永年私財法於いて亜亞唖".decode("utf-8"))
    score = this.estimateDifficulty()
    print score
    this.splitSentences("このさい、この際、この文章の難易度を判定して下さい。".decode("utf-8"))
    score = this.estimateDifficulty()
    print score
    this.close()
    print "THE END"

    