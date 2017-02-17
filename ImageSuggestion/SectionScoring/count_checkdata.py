import sys
import os
import codecs
import regex as re
from testSample import test_samples

dirnames = [
    (u"docs\\1_20\\",u"dicts\\1_20_all.txt"),
    (u"docs\\21_40\\",u"dicts\\21_40_all.txt"),
    (u"docs\\41_60\\",u"dicts\\41_60_all.txt"),
    (u"docs\\61_80\\",u"dicts\\61_80_all.txt"),
    (u"docs\\81_100\\",u"dicts\\81_100_all.txt"),
]

def count_checkdata(dirname,outputfilename):
    a,b,c,d = 0,0,0,0
    ma = re.compile(u"a,b,c,d = (?P<a>.*),(?P<b>.*),(?P<c>.*),(?P<d>.*)\n")
    for dir in os.listdir(dirname):
        if u"-checker" in dir:
            with codecs.open(dirname+u"\\"+dir,mode=u"r",encoding=u"utf-8-sig") as file:
                matchobj = ma.match(file.readlines()[-4])
                a += int(matchobj.group(u"a"))
                b += int(matchobj.group(u"b"))
                c += int(matchobj.group(u"c"))
                d += int(matchobj.group(u"d"))
    with codecs.open(outputfilename,"a","utf-8-sig") as file:
        file.write(u"in "+dirname+u", a,b,c,d = %d,%d,%d,%d\n"%(a,b,c,d))
    return a,b,c,d

if __name__ == "__main__":
    point = 0
    alls = 0
    argv = sys.argv
    outdirname = u"no_hiragana_dicts_0.0005_with_paraSentence"
    if not os.path.exists(outdirname):
        os.mkdir(outdirname)
    for dirname in dirnames:
        #with codecs.open(u"dictlist.txt",u"w","utf-8-sig") as file:
        #    file.write(u"\n".join([l[1] for l in dirnames if l is not dirname]))
        test_samples(dirname[0],outdirname)
    a,b,c,d = count_checkdata(outdirname,u"checklist.txt")
    with codecs.open(outdirname+"\\checklist.txt","a","utf-8-sig") as file:
        file.write(u"in all, a,b,c,d = %d,%d,%d,%d\n"%(a,b,c,d))
        precision = (float(d)/(c+d))if c+d != 0 else 0.0
        recall = (float(d)/(b+d))if b+d != 0 else 0.0
        if (precision + recall) != 0:
            fvalue = 2.0*precision*recall/(precision+recall)
        else:
            fvalue = 0.0
        file.write(u"      precision = %f\n"%(precision))
        file.write(u"         recall = %f\n"%(recall))
        file.write(u"         fvalue = %f\n"%(fvalue))