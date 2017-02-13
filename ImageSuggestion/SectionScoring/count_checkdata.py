import regex as re
import os
import codecs
from testSample import test_samples

dirnames = [
    (u"docs\\1_20\\",u"dicts\\1_20_all.txt"),
    (u"docs\\21_40\\",u"dicts\\21_40_all.txt"),
    (u"docs\\41_60\\",u"dicts\\41_60_all.txt"),
    (u"docs\\61_80\\",u"dicts\\61_80_all.txt"),
    (u"docs\\81_100\\",u"dicts\\81_100_all.txt"),
]

def count_checkdata(dirname):
    alls = 0
    point = 0
    ma = re.compile(u" check is (?<point>.*) / (?<all>.*)")
    for dir in os.listdir(dirname):
        if u"-checker_3" in dir:
            with codecs.open(dirname+u"\\"+dir,mode=u"r",encoding=u"utf-8-sig") as file:
                matchobj = ma.match(file.readlines()[-1])
                alls += int(matchobj.group(u"all"))
                point += int(matchobj.group(u"point"))
    with codecs.open("checklist.txt","a","utf-8-sig") as file:
        file.write(u"in "+dirname+u", check is %d / %d\n"%(point,alls))
    return point,alls

if __name__ == "__main__":
    point = 0
    alls = 0
    for dirname in dirnames:
#        with codecs.open(u"dictlist.txt",u"w","utf-8-sig") as file:
#            file.write(u"\n".join([l[1] for l in dirnames if l is not dirname]))
#        test_samples(dirname[0])
        subpoint,suballs = count_checkdata(dirname[0])
        point += subpoint
        alls += suballs
    with codecs.open("checklist.txt","a","utf-8-sig") as file:
        file.write(u"in all, check is %d / %d\n"%(point,alls))