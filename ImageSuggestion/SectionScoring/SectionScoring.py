# -*- encoding:utf-8-sig -*-
import sys
import codecs
#from html.parser import HTMLParser
from sptext import SpText
import functools
from functools import reduce
import regex as re
import os
from os import path
import glob

PARA_GRAPH_SCORE = 1
PARA_TABLE_SCORE = 1
DESCRIPTION_SCORE = 1
TAGLIST = [
    "table","picture","graph","flow"
]

def parseHTML(htmltext):
    #lxml? BeautifulSoup? HTMLparser? You use you want.
    #htmlparser = HTMLParser()
    #parsedhtml = htmlparser.feed(htmltext)
    return "parsed html"

def html2text(parsedhtml):
    #If you want, do Unicode Nomalize
    #unicodedata.nomalize(parsedhtml)

    #How?
    return "raw text"

def split_sections(rawText):
    """hogehoge"""
    sections = []

    #split by "\n\n" or "\n\n\n" or "\n\n\n\n" ...
    for line in re.split(r"\n{2,}",rawText):
        sections.append(SpText(line))
    return sections

def split_sentences(section):
    answerlist = []
    st = section.text.strip()
    #asre = ur"(?P<all>(?:[^?u?v?B]*(?P<rec>[?u](?:[^?u?v]*|(?P&rec))*[?v]))*.*?(\Z))"
    sentenceRe = re.compile("")
    for line in st.split("\n"):
        sentencelist = [SpText(i[0]) for i in sentenceRe.findall(line.strip())]
        sentencelist = filter(lambda s:len(s.text) > 0,sentencelist)
        answerlist.extend(sentencelist if len(sentencelist) else [SpText(line.strip())])
    return answerlist

def get_paralell(text):
    return []

def is_numerical(para):
    return True

def scoring_clueword(text):
    ans = dict.fromkeys(TAGLIST,0.0)
    #sun score
    return ans

def scoring_keyexp(text):
    ans = dict.fromkeys(TAGLIST,0.0)
    #sun score
    return ans

if __name__==u"__main__":
    #HTMLFile:unicode
    htmlfile_name = "sample.html"
    try:
        with codecs.open(htmlfile_name,"r","utf-8-sig") as htmlfile:
            htmltext = str(htmlfile.read())
    except IOError as e:
        print("in:"+e.filename)
        print(e)
        raise

    #HTMLText:unicode:unicode (and more?)
    parsedhtml = parseHTML(htmltext)
    rawtext = html2text(parsedhtml)

    #RawText:unicode:list(sptext?unicode)
    sections = split_sections(rawtext)

    for section in sections:
        #Section(sptext?unicode):list(sptext?unicode)
        sentences = split_sentences(section)

        #scoring
        scores = dict.fromkeys(TAGLIST,0.0) #score[tagname] -> score
        for sentence in sentences:
            #*has Paralell?
            paras = get_paralell(sentence.text)
            if len(paras) > 0:
                for para in paras:
                    #is about numerical? or sentential?
                    if is_numerical(para):
                        scores["graph"] += PARA_GRAPH_SCORE
                    else:
                        scores["table"] += PARA_TABLE_SCORE

            #*has ClueWord?
            clueword_score = scoring_clueword(sentence.text)
            for key in scores:
                scores[key] += clueword_score[key]

            #*has keyExpression?
            keyexp_score = scoring_keyexp(sentence.text)
            for key in scores:
                scores[key] += keyexp_score[key]

            #*is Description about paralell word?
            for para in allpara:
                if is_description(sentence.text,para):
                    scores["table"] += DESCRIPTION_SCORE

        #sum score and set in Section
        section.scores = scores
        section.score = reduce(lambda a,b:a+b,scores.values())

    #sort Sections by score
    sorted_section = sorted(sections,key=lambda section:section.score,reverse=True)

    #show answer and...
    for section in sorted_section:
        print("Score:" + str(section.score))
        print(section.text)
        for item in section.scores.items():
            print(item[0] +""+ str(item[1]))

    # F I N I S H ! ( O S H I M A I ! )