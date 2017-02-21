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
    types = [
        u'True-Negative',
        u'False-Negative',
        u'False-Positive',
        u'True-Positive'
    ]
    typecount = dict.fromkeys(types,0)
    res = []
    for type_ in types:
        res.append(re.compile(type_+u':(.*)'))
    for dir in os.listdir(dirname):
        if u"-checker" in dir:
            with codecs.open(dirname+u"\\"+dir,u"r",encoding=u"utf-8-sig") as file:
                text = file.read()
                for typere,type_ in zip(res,types):
                    typecount[type_] += float(typere.search(text).group(1))
    return typecount

if __name__ == "__main__":
    point = 0
    alls = 0
    argv = sys.argv
    outdirname = u"new3_tf_genkei_0.0"
    if not os.path.exists(outdirname):
        os.mkdir(outdirname)
    for dirname in dirnames:
        #with codecs.open(u"dictlist.txt",u"w","utf-8-sig") as file:
        #    file.write(u"\n".join([l[1] for l in dirnames if l is not dirname]))
        test_samples(dirname[0],outdirname)
        pass
    typecount = count_checkdata(outdirname,u"checklist.txt")
    with codecs.open(outdirname+"\\checklist.txt","a","utf-8-sig") as file:
        file.write(u"in all:\n")
        for type_,count in typecount.iteritems():
            file.write(type_+u' : '+unicode(count)+u'\n')
        if typecount[u'True-Positive'] == 0:
            precision = 0
        else:
            precision = typecount[u'True-Positive'] / (typecount[u'True-Positive']+typecount[u'False-Positive'])
        if typecount[u'True-Positive'] + typecount[u'False-Negative'] == 0:
            recall = 0
        else:
            recall = typecount[u'True-Positive'] / (typecount[u'True-Positive']+typecount[u'False-Negative'])
        if precision + recall == 0:
            fvalue = 0
        else:
            fvalue = (2.0*precision*recall) / (precision+recall)
        file.write(u"      precision = %f\n"%(precision))
        file.write(u"         recall = %f\n"%(recall))
        file.write(u"         fvalue = %f\n"%(fvalue))