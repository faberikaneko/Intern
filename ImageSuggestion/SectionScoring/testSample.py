# -*- encoding:utf-8-sig -*-

import unittest

from SectionScoring import filescoring
from SectionScoring import readsections,sectionscoring,writescore
from multiprocessing import Pool
import os

import regex as re
from imagescore import ImageScore

import codecs

def testscoring(inputfilename,outputfilename):
    sections = readsections(inputfilename)
    anssections = sectionscoring(sections,inputfilename)
    sorted_section = sorted(anssections.childs,key=lambda section:section.score,reverse=True)
    flags = re.compile(ur"Flag：：(?<image>\d)(?<table>\d)(?<graph>\d)(?<flow>\d)")
    outfile = codecs.open(outputfilename,mode="w",encoding="utf-8-sig")
    allcheker = 0
    startflag = True
    for section in sorted_section:
        if startflag:
            startflag = False
        else:
            outfile.write(u"\n")
        outfile.write(section.text+u"\n")
        for key in ImageScore.taglist:
            outfile.write(key+u" : "+unicode(section.scores.get(key))+u"\n")
        if not len(section.childs) > 0:
            outfile.write(u"wrong file\n")
            pass
        else:
            flagmatch = flags.match(section.childs[0].text)
            if not flagmatch:
                outfile.write(u"worng file\n")
                pass
            else:
                teacherscore = {}
                count = 0
                for key in ImageScore.taglist:
                    teacher = int(flagmatch.group(key))
                    teacherscore[key] = teacher
                    if teacher:
                        count+=1
                sortscore = sorted(section.scores.items(),key=lambda s:s[1],reverse=True)
                if not 1 == teacherscore.get(sortscore[0][0]):
                    outfile.write(u"bad\n")
                    pass
                else:
                    if (count >= 2) and 1 == teacherscore.get(sortscore[1][0]):
                        outfile.write(u"bad\n")
                        pass
                    else:
                        outfile.write(u"good!\n")
                        allcheker += 1 
                        pass
    outfile.write(u"\n\n check is "+unicode(allcheker)+u" / " + unicode(len(sections.childs)))
    outfile.close()


if __name__ == '__main__':
    MAXTHREAD = 8
    p = Pool(MAXTHREAD)
    for dir in os.listdir(u"tests"):
        if not u"-answer" in dir:
            filename,exe = os.path.splitext(dir)
            inputfilename = os.path.join(ur"tests\\",filename+exe)
            outputfilename = os.path.join(ur"check\\",filename+u"-checker"+exe)
            p.apply_async(func=testscoring,
                            args=(inputfilename,outputfilename),
            )
            #testscoring(inputfilename,outputfilename)
    p.close()
    p.join()
    #section_scoring(u"sample.txt",u"sample-ans.txt")
