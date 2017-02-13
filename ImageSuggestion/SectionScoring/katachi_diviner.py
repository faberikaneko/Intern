import sys
import ast
import codecs
import regex as re

if __name__ == "__main__":
    katachi2 = {}
    linere = re.compile(ur"(?P<key>.*?):(?P<dict>.*)")
    with codecs.open(u'katachi.txt','r','utf-8-sig') as file:
        readlines = file.readlines()
    for line in readlines:
        rematch = linere.match(line)
        if rematch:
            d = ast.literal_eval(rematch.group(u'dict'))
            d2 = {}
            for key in d:
                d2[key] = d[key][1] / float(d[key][0]+d[key][1])
            d2[u'all'] = d[key][0] + d[key][1]
            katachi2[rematch.group(u'key')] = d2
        print(line)
    li = sorted(katachi2.items(),key=lambda x:x[1][u'all'],reverse=False)
    with codecs.open('katachi2.txt','w','utf-8-sig') as file:
        for le in li:
            file.write(u'{'+le[0]+u':'+str(le[1])+u'}\n')