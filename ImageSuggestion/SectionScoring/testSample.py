import unittest

from SectionScoring import section_scoring
from multiprocessing import Pool
import os

if __name__ == '__main__':
    MAXTHREAD = 8
    p = Pool(MAXTHREAD)
    for dir in os.listdir(u"tests"):
        if not u"-answer" in dir:
            filename,exe = os.path.splitext(dir)
            inputfilename = os.path.join(ur"tests\\",filename+exe)
            outputfilename = os.path.join(ur"tests\\",filename+u"-answer"+exe)
        #    p.apply_async(func=section_scoring,
        #                    args=(inputfilename,outputfilename),
        #    )
            section_scoring(inputfilename,outputfilename)
    p.close()
    p.join()
    #section_scoring(u"sample.txt",u"sample-ans.txt")
    for dir in os.listdir(u"tests"):
        if u"-answer" in dir:
            pass
