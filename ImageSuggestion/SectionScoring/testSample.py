# -*- encoding:utf-8 -*-

from SectionScoring import filescoring,readsections,sectionscoring
from SectionScoring import writesection,writescore
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
SCORE_LIMIT = 0.0005
IGNORE_TYPE = True

def writefile(section,type,dirname=u'abcd\\'):
    abcddir = dirname
    filename = os.path.join(abcddir,type+u'.txt')
    if not os.path.exists(abcddir):
        os.mkdir(abcddir)
    with codecs.open(filename,mode='a',encoding='utf-8-sig') as file:
        file.write(writesection(section)+u'\n')

def testscoring(inputfilename,outputfilename):
    typemessage={
        u'TN':u'True-Negative',
        u'FN':u'False-Negative',
        u'FP':u'False-Positive',
        u'TP':u'True-Positive'
    }
    dirname = outputfilename.rsplit(u'\\',1)[0]+u'\\'
    sections = readsections(inputfilename)
    anssections = sectionscoring(sections,inputfilename)
    sorted_section = sorted(anssections.childs,key=lambda section:section.score,reverse=True)
    flags = re.compile(ur"Ｆｌａｇ：：(?<image>.)(?<table>.)(?<graph>.)(?<flow>.)")
    outfile = codecs.open(outputfilename,mode="w",encoding="utf-8-sig")
    typecount = dict.fromkeys([u'TN',u'FN',u'FP',u'TP'],0)
    startflag = True
    ignorecount = 0.0
    for section in sorted_section:
        if startflag:
            startflag = False
        else:
            outfile.write(u"\n\n")
        outfile.write(writesection(section))
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
                        type_ = u'TN'
                    else:
                        type_ = u'FN'
                else:
                    if count == 0:
                        type_ = u'FP'
                    else:
                        if IGNORE_TYPE or teacherscore[sortscore[0][0]] == 1:
                            type_ = u'TP'
                        else:
                            type_ = u'FP'
                outfile.write(typemessage[type_])
                typecount[type_] += 1.0
                writefile(section,type_,dirname+'tfpn\\')
    outfile.write(u'\n\n')
    for key,value in typecount.iteritems():
        outfile.write(u'{:s}:{:d}\n'.format(typemessage[key],int(value)))
    if typecount[u'TP'] == 0:
        precision = 0
    else:
        precision = typecount[u'TP'] / (typecount[u'TP']+typecount[u'FP'])
    if typecount[u'TP'] == 0:
        recall = 0
    else:
        recall = typecount[u'TP'] / (typecount[u'TP']+typecount[u'FN'])
    if precision + recall == 0:
        fvalue = 0
    else:
        fvalue = (2.0*precision*recall)/(precision+recall)
    outfile.write(u"precision = %f\n"%(precision))
    outfile.write(u"recall = %f\n"%(recall))
    outfile.write(u"fvalue = %f"%(fvalue))
    outfile.close()
    logger.debug(u"finish %s"%(inputfilename))

def worker():
    while True:
        t = q.get()
        try:
            testscoring(t[0],t[1])
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
        if not u"-checker" in dir:
            filename,exe = os.path.splitext(dir)
            inputfilename = os.path.join(dirname,filename+exe)
            outputfilename = os.path.join(outdirname,filename+u"-checker"+exe)
            #answer = os.path.join(outdirname,filename+u"-answer"+exe)
            q.put((inputfilename,outputfilename))
            #testscoring(inputfilename,outputfilename,answer)
    q.join()
    #testscoring(ur"docs\\1_20.txt",u"anss\\1_20_check.txt",u"anss\\1_20_answer.txt")

if __name__ == '__main__':
    test_samples(u"docs\\1_20\\",u"newdicts\\")