# -*- encoding:utf-8-sig -*-

from __future__ import unicode_literals

import sys
from os import listdir
from codecs import open

import regex as re
from pyknp import Juman

from SectionScoring import readsections, split_sentences
from imagescore import ImageScore

katachi = {}
def covariance_check(filename):
    getatters = [
        u'bunrui',
        u'genkei',
        u'hinsi',
        u'katuyou1',
        u'katuyou2',
    ]
    juman = Juman(option=u'-B -e2')
    flags = re.compile(ur"Flag：：(?<image>\d)(?<table>\d)(?<graph>\d)(?<flow>\d)")

    sections = readsections(filename)
    for section in sections.childs:
        sentences = split_sentences(section)
        flagmatch = flags.match(sentences[0].text)
        if flagmatch:
            for sentence in sentences[1:]:
                result = juman.analysis(sentence.text)
                for morph in result.mrph_list():
                    for attr in getatters:
                        s = getattr(morph,attr)
                        if not s in katachi:
                            katachi[s] = dict.fromkeys(ImageScore.taglist)
                            for tag in ImageScore.taglist:
                                katachi[s][tag] = [0,0]
                        for tag in ImageScore.taglist:
                            katachi[s][tag][int(flagmatch.group(tag))] += 1
    print(filename)
        #add scores in dict
    pass

if __name__ == '__main__':
    docdirs = [
        u'docs\\1_20\\',
        u'docs\\21_40\\',
        u'docs\\41_60\\',
        u'docs\\61_80\\',
        u'docs\\81_100\\',
    ]
    filelist = []
    for docname in docdirs:
        for filename in listdir(docname):
            if not (u'answer' in filename or u'check' in filename):
                covariance_check(docname+filename)
    with open(u'katachi.txt',u'w',u'utf-8-sig') as file:
        for item in katachi.items():
            file.write(item[0]+u':')
            file.write(str(item[1])+u'\n')