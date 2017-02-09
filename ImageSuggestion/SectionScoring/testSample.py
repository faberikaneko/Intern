# -*- encoding:utf-8-sig -*-

import unittest

from SectionScoring import filescoring
from SectionScoring import readsections,sectionscoring,writescore
from multiprocessing import Pool
import os

import regex as re
from imagescore import ImageScore

import codecs
from logging import getLogger, StreamHandler, Formatter, DEBUG
formatter = Formatter(fmt=u"[%(levelname)s] %(message)s")
handler = StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(DEBUG)
logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(handler)

def testscoring(inputfilename,outputfilename,answer):
    sections = readsections(inputfilename)
    anssections = sectionscoring(sections,inputfilename)
    writescore(sections,answer)
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
                if count == 0:
                    if sortscore[0][1] <= 0.0:
                        allcheker += 1
                        outfile.write(u"good!\n")
                    else:
                        outfile.write(u"bad\n")
                else:
                    if not 1 == teacherscore.get(sortscore[0][0]):
                        outfile.write(u"bad\n")
                        pass
                    else:
                        if False and (count >= 2) and not 1 == teacherscore.get(sortscore[1][0]):
                            outfile.write(u"bad\n")
                            pass
                        else:
                            outfile.write(u"good!\n")
                            allcheker += 1 
                            pass
    outfile.write(u"\n\n check is "+unicode(allcheker)+u" / " + unicode(len(sections.childs)))
    outfile.close()
    logger.debug(u"finish %s"%(inputfilename))


if __name__ == '__main__':
    MAXTHREAD = 8
    p = Pool(MAXTHREAD)
    for dir in os.listdir(u"afters"):
        if not (u"-answer" in dir or u"-checker" in dir):
            filename,exe = os.path.splitext(dir)
            inputfilename = os.path.join(ur"afters\\",filename+exe)
            outputfilename = os.path.join(ur"afters\\",filename+u"-checker"+exe)
            answer = os.path.join(ur"afters\\",filename+u"-answer"+exe)
            #p.apply_async(func=testscoring,
            #                args=(inputfilename,outputfilename,answer),
            #)
            #testscoring(inputfilename,outputfilename,answer)
    p.close()
    p.join()
    testscoring(ur"afters-0.txt",u"afters-0-check.txt",u"afters-0-ans.txt")
