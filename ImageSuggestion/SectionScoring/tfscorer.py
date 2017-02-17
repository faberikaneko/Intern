# -*- encoding:utf-8 -*-

import os
import codecs
import regex as re

def tfscorer(dirname):
    scorere = re.compile(u'^Score:(.*)$',flags=re.U|re.M)
    types = [
        u'True-Positive',
        u'True-Negative',
        u'False-Negative',
        u'False-Positive',
    ]
    typescores = dict.fromkeys(types)
    for type_ in types:
        typescores[type_] = list()
    for filename in os.listdir(dirname):
        filename = dirname + filename
        with codecs.open(filename,encoding='utf-8-sig') as file:
            texts = file.read().split('\n\n')
            for text in texts:
                scorematch = scorere.search(text)
                if scorematch:
                    for type_ in types:
                        if type_ in text:
                            typescores[type_].append(float(scorematch.group(1)))
    for name,list_ in typescores.iteritems():
        with codecs.open(name+u'.csv',mode='w',encoding=u'utf-8-sig') as file:
            for value in list_:
                file.write(unicode(value)+u'\n')

if __name__ == '__main__':
    tfscorer(u'lineword_dicts_0.0005\\')