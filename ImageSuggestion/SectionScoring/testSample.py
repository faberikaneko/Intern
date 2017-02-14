# -*- encoding:utf-8-sig -*-

from SectionScoring import filescoring,readsections,sectionscoring,writescore
from Queue import Queue
from threading import Thread
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

global SCORE_LIMIT
SCORE_LIMIT = 0.01

def testscoring(inputfilename,outputfilename,answer):
    sections = readsections(inputfilename)
    anssections = sectionscoring(sections,inputfilename)
    writescore(sections,answer)
    sorted_section = sorted(anssections.childs,key=lambda section:section.score,reverse=True)
    flags = re.compile(ur"Flag：：(?<image>\d)(?<table>\d)(?<graph>\d)(?<flow>\d)")
    outfile = codecs.open(outputfilename,mode="w",encoding="utf-8-sig")
    a,b,c,d = 0,0,0,0
    startflag = True
    ignorecount = 0
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
                global SCORE_LIMIT
                if section.score <= SCORE_LIMIT:
                    if count == 0:#A:nono
                        outfile.write(u"no, pattern A\n")
                        a += 1
                    else:
                        outfile.write(u"BAD, pattern B\n")
                        b += 1
                else:
                    if count == 0:
                        outfile.write(u"BAD, pattern C\n")
                        c += 1
                    else:
                        outfile.write(u"good, pattern D\n")
                        d += 1
    outfile.write(u"\n\na,b,c,d = %d,%d,%d,%d\n"%(a,b,c,d))
    precision = (float(d)/(c+d)) if c+d != 0 else 0
    recall = (float(d)/(b+d)) if b+d != 0 else 0
    outfile.write(u"precision = %f\n"%(precision))
    outfile.write(u"recall = %f\n"%(recall))
    fvalue = (2.0*precision*recall/(precision+recall)) if precision+recall != 0 else 0
    outfile.write(u"fvalue = %f"%(fvalue))
    outfile.close()
    logger.debug(u"finish %s"%(inputfilename))

def worker():
    while True:
        t = q.get()
        try:
            testscoring(t[0],t[1],t[2])
        except Exception as e:
            with codecs.open(u"error.txt",u"a",u"utf-8-sig") as file:
                file.write(u"in %s,\n"%t[0])
                file.write(e.message)
            raise
        finally:
            q.task_done()


MAXTHREAD = 4
q = Queue(MAXTHREAD)
def test_samples(dirname,outdirname):
    for i in range(MAXTHREAD):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
    for dir in os.listdir(dirname):
        if not (u"-answer" in dir or u"-checker" in dir):
            filename,exe = os.path.splitext(dir)
            inputfilename = os.path.join(dirname,filename+exe)
            outputfilename = os.path.join(outdirname,filename+u"-checker"+exe)
            answer = os.path.join(outdirname,filename+u"-answer"+exe)
            q.put((inputfilename,outputfilename,answer))
            #testscoring(inputfilename,outputfilename,answer)
    q.join()
    #testscoring(ur"docs\\1_20.txt",u"anss\\1_20_check.txt",u"anss\\1_20_answer.txt")

if __name__ == '__main__':
    test_samples(u"docs\\1_20\\",u"newdicts\\")