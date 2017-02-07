# -*- encoding:utf-8-sig -*-

import sys
import codecs
import regex as re
import unicodedata
from sptext import SpText
from HTMLParser import HTMLParser,HTMLParseError
from ParalellFinder import sentence_paralell_finder as parafinder
import os
import threading
from multiprocessing import Pool
from imagescore import ImageScore
import ScoringClass

from logging import getLogger, StreamHandler, Formatter, DEBUG
formatter = Formatter(fmt=u"[%(levelname)s] %(message)s")
handler = StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(DEBUG)
#config logger
logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(handler)

#TODO: The Best Score Of Paralell Words
PARA_GRAPH_SCORE = 0.05
PARA_TABLE_SCORE = 0.05
DESCRIPTION_SCORE = 0.05
TAGLIST = ImageScore.taglist

def text_normalizer(rawtext):
    """rawtext: unicode -> normalized_text: unicode"""
    #normalize text
    normalized_text = unicodedata.normalize(u"NFKC",rawtext)

    #half charactor -> full charactor
    #\r\n or \r -> \n
    #., -> ，．(without number point)
    #<>[]{} ()-> ＜＞［］｛｝（）
    #!"#$%&'=~|?_-^\/;:+*
    # -> ！”＃＄％＆’＝～｜？＿‐￥・／；：＋＊
    replace_halfres = [
        #return
        (ur"\r\n|\r",u"\n"),
        #piriod and comma
        (ur"(?:(?<!\d)|\A)\.(?!\d)",u"．"),
        (ur",",u"，"),
        #bracket
        (ur"<",u"＜"),
        (ur">",u"＞"),
        (ur"{",u"｛"),
        (ur"}",u"｝"),
        (ur"\[",u"［"),
        (ur"\]",u"］"),
        (ur"\(",u"（"),
        (ur"\)",u"）"),
        #other marks
        (ur"!",u"！"),
        (ur"#",u"＃"),
        (ur"%",u"％"),
        (ur"'",u"’"),
        (ur"=",u"＝"),
        (ur"~",u"～"),
        (ur"_",u"＿"),
        (ur"-",u"－"),
        (ur"/",u"／"),
        (ur";",u"；"),
        (ur":",u"："),
        #special marks
        (ur"\"",u"”"),
        (ur"\|",u"｜"),
        (ur"\?",u"？"),
        (ur"\$",u"＄"),
        (ur"\+",u"＋"),
        (ur"\*",u"＊"),
        (ur"\^",u"＾"),
        (ur"\\",u"￥"),
    ]
    for replace_halfre in replace_halfres:
        fromre = replace_halfre[0]
        tore = replace_halfre[1]
        normalized_text = re.sub(fromre,tore,normalized_text)
    return normalized_text

def split_sections(text):
    """text: SpText -> list[SpText]"""
    sections = []

    #split by "\n\n" or "\n\n\n" or "\n\n\n\n" ...
    index = 1
    for line in re.split(ur"\n{2,}",text):
        section = SpText(line)
        section.No = index
        sections.append(section)
        index += 1
    return sections

def split_sentences(section):
    """section: SpText -> list[SpText]"""
    answerlist = []
    st = section.text.strip()
    sentenceRe = re.compile(ur"(?P<all>(?:[^「」（）。]*(?P<rec>[「（](?:[^「」（）]*|(?P&rec))*[」）]))*.*?(?:。|\Z))")
    for line in st.split(ur"\n"):
        sentencelist = [SpText(i[0]) for i in sentenceRe.findall(line.strip())]
        sentencelist = list(filter(lambda s:len(s.text) > 0,sentencelist))
        answerlist.extend(sentencelist if len(sentencelist) else [SpText(line.strip())])
    return answerlist

def get_paralell(text):
    """sentence: sptext -> list[list[unicode]]?"""
    paralist = parafinder(text)
    answer = []
    for paraitem in paralist:
        anslist = list(b.word for b in paraitem[0].keys())
        answer.append(anslist)
        pass

    #maybe use Paralell Finder
    return answer

def is_numerical(paras):
    """return True is para has description about values"""
    numre = re.compile("[0-9０-９]")
    nums = 0
    for para in paras:
        if len(numre.findall(para)) > 0:
            nums += len(numre.findall(para))
    return True if nums >= len(paras) else False

def scoring_clueword(text):
    """By ScorgingClass, scoring to text:unicode"""
    anslist = []
    #sum score
    for clueword in ScoringClass.clueword.items():
        index = 0
        while text.find(clueword[0],index) >= 0:
            anslist.append(clueword)
            index += text.find(clueword[0],index)+len(clueword[0])
    return anslist

def has_description(childs,word):
    """childs: list[bunsetsu], word: unicode -> bool
        return True if text descript about word."""
    if any([b.description_about(word) for b in childs]):
        return True
    return False

def section_scoring(fromfilename,tofilename):
    #textfile:unicode
    readfile_name = fromfilename
    answerfilen_name = tofilename
    logger.debug(u"from:"+fromfilename+u", to:"+tofilename)

    try:
        with codecs.open(readfile_name,u"r",u"utf-8-sig") as htmlfile:
            rawtext = unicode(htmlfile.read())
    except IOError as e:
        print(u"in:"+e.filename)
        print(e)
        raise

    #normalize text 
    normal_text = text_normalizer(rawtext)

    #RawText:unicode:list(sptext?unicode)
    sections = split_sections(normal_text)

    logger.debug(u"%s's section#:%d start"%(readfile_name,len(sections)))
    for section in sections:
        logger.debug(u"in section:%2d/%2d at %s"\
                    %(sections.index(section)+1,len(sections),readfile_name))
        #Section(sptext?unicode):list(sptext?unicode)
        sentences = split_sentences(section)
        section.paralells = []
        section.descriptions = []
        section.cluewords = []

        #scoring
        scores = dict.fromkeys(TAGLIST,0.0) #score[tagname] -> score
        allpara = set()
        for sentence in sentences:
            #*has Paralell?
            paras = get_paralell(sentence)
            section.paralells.extend(paras)
            if len(paras) > 0:
                allpara = allpara.union(set(reduce(lambda a,b:a+b,paras)))
                for para in paras:
                    #is about numerical? or sentential?
                    if is_numerical(para):
                        scores[u"graph"] += PARA_GRAPH_SCORE*len(para)
                    else:
                        scores[u"table"] += PARA_TABLE_SCORE*len(para)

            #*has ClueWord and/or keyExp?
            clueword_scores = scoring_clueword(sentence.text)
            for clueword_score in clueword_scores:
                section.cluewords.append(clueword_score[0])
                for key in scores:
                    scores[key] += clueword_score[1].dict[key]

            #*is Description about paralell word?
            for para in allpara:
                if has_description(sentence.childs,para):
                    section.descriptions.append(para)
                    scores[u"table"] += DESCRIPTION_SCORE

        #sum score and set in Section
        section.scores = scores
        section.score = float(reduce(lambda a,b:a+b,scores.values()))

    #sort Sections by score
    sorted_section = sorted(sections,key=lambda section:section.score,reverse=True)

    logger.debug(u"write answer to %s"%(answerfilen_name))
    #show answer and...
    with codecs.open(answerfilen_name,u"w",encoding=u"utf-8-sig")\
    as answerfile:
        stflag = True
        for section in sorted_section:
            if stflag:
                stflag = False
            else:
                answerfile.write(u"\n")
            answerfile.write(u"In Section %d, Score:%f"%(section.No,section.score)+u"\n")
            answerfile.write(section.text+u"\n")
            for paraitem in section.paralells:
                answerfile.write(",".join(paraitem)+u"\n")
            for descitem in section.descriptions:
                answerfile.write(u"description : "+descitem+u"\n")
            answerfile.write(u"clueword:\n")
            answerfile.write(u", ".join(section.cluewords)+u"\n")
            for item in section.scores.items():
                answerfile.write(item[0]+u" : "+unicode(item[1])+u"\n")
    logger.debug(u"file:%s is end."%inputfilename)
    # F I N I S H ! ( O S H I M A I ! )

if __name__==u"__main__":
    threads = []
    p = Pool(5)
    for dir in os.listdir(u"datas"):
        if not u"-answer" in dir:
            filename,exe = os.path.splitext(dir)
            inputfilename = os.path.join(ur"datas\\",filename+exe)
            outputfilename = os.path.join(ur"datas\\",filename+u"-answer"+exe)
            p.apply_async(func=section_scoring,
                          args=(inputfilename,outputfilename),
            )
    p.close()
    p.join()