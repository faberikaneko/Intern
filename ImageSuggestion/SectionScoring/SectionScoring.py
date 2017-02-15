# -*- encoding:utf-8-sig -*-

import sys
import codecs
import regex as re
import unicodedata
from sptext import SpText
from ParalellFinder import sentence_paralell_finder as parafinder
import os
import threading
from multiprocessing import Pool

from pyknp import Juman

from imagescore import ImageScore
from ScoringMod import ScoringClass

#config logger
from logging import getLogger, StreamHandler, Formatter, DEBUG
formatter = Formatter(fmt=u"[%(levelname)s] %(message)s")
handler = StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(DEBUG)
logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(handler)

#TODO: The Best Score Of Paralell Words
SCORE={
    'PARA_SENTENCE':0.02,
    'PARA_GRAPH':0.00,
    'PARA_TABLE':0.01,
    'PARA_IMAGE':0.0,
    'DESC_SENT':0.0,
    'DESC_WORD':0.0,
}

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
        #http
        (ur"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+",u"(URLS)"),
        #return
        (ur"\r\n|\r|\n",u"\n"),
        #piriod and comma
        (ur"(?:(?<!\d)|\A)\.(?!\d)",u"．"),
        (ur",",u""),
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
        (ur"-|–",u"－"),
        (ur"/",u"／"),
        (ur";",u"；"),
        (ur":",u"："),
        (u'•|·|･','・'),
        #special marks
        (ur"\"",u"”"),
        (ur"\|",u"｜"),
        (ur"\?",u"？"),
        (ur"\$",u"＄"),
        (ur"\+",u"＋"),
        (ur"\*",u"＊"),
        (ur"\^",u"＾"),
        (ur"\\",u"￥"),
        #blank
        (ur"\p{Zs}",u""),
    ]
    for replace_halfre in replace_halfres:
        fromre = replace_halfre[0]
        tore = replace_halfre[1]
        normalized_text = re.sub(fromre,tore,normalized_text)

    #encode escape
    try:
        normalized_text.encode(u"cp932")
    except UnicodeEncodeError as e:
        newline = u""
        for c in normalized_text:
            try:
                c.encode(u"cp932")
                newline += c
            except UnicodeEncodeError:
                newline += u"？"
        normalized_text = newline

    return normalized_text

def split_sections(text):
    """text: SpText -> list[SpText]"""
    section_child = []

    #split by "\n\n" or "\n\n\n" or "\n\n\n\n" ...
    index = 1
    for line in re.split(ur"(?:\n\p{Zs}*)+\n",text):
        if len(line) > 0:
            section = SpText(line)
            section.No = index
            section_child.append(section)
            index += 1
    sections = SpText(text,childs=section_child)
    return sections

def split_sentences(section):
    """section: SpText -> list[SpText]"""
    answerlist = []
    st = section.text.strip()
    sentenceRe = re.compile(ur"""
    (?P<all>
        (?:[^「」（）。]*
            (?P<rec>[「（]   (?:[^「」（）]*|(?P&rec))*   [」）])
        )*
        [^「」（）。]*(?:。|\Z|\n)
    )""",
        flags=re.X)
    for line in st.split(u"\n"):
        sentencelist = [SpText(i[0]) for i in sentenceRe.findall(line.strip())]
        sentencelist = list(filter(lambda s:len(s.text) > 0,sentencelist))
        answerlist.extend(sentencelist if len(sentencelist) else [SpText(line.strip())])
    return answerlist

def get_paralell(sentence):
    """sentence: sptext
     -> [({paralell_word:discription[]},[toroot],[toleaf])]
        :mini_bunsetsu"""
    paralist = parafinder(sentence)
    return paralist

def is_numerical(para):
    """return True is para has description about values"""
    numre = re.compile("[0-9０-９]")
    nums = 0
    for descriptions in para[0].values():
        for description in descriptions:
            if len(numre.findall(description.word)) > 0:
                nums += len(numre.findall(description.word))
    return True if nums >= len(para[0]) else False

def scoring_clueword(section):
    """By ScorgingClass, scoring to section:SpText"""
    anslist = []
    #sum score
    d = ScoringClass.get_clueword()
    morphlist = set()
    for sentence in section.childs:
        for mini in sentence.childs:
            morphlist = morphlist | set(mini.morphs)
    for morph in morphlist:
        for clueword in d.items():
            if morph.genkei == clueword[0]:
                anslist.append(clueword)
                break
    return anslist

def has_description(childs,word):
    """childs: list[bunsetsu], word: unicode -> bool
        return True if text descript about word."""
    if any([b.description_about(word) for b in childs]):
        return True
    return False

def get_section_paralells(section):
    numnum = 0
    markf = {}
    renum = re.compile(ur"\p{N}",flags=re.U|re.I)
    for sentence in section.childs:
        if renum.match(sentence.text):
            numnum += 1
        else:
            if len(sentence.text) >= 1:
                if sentence.text[0] in markf:
                    markf[sentence.text[0]] += 1
                else:
                    markf[sentence.text[0]] = 1
    dotnum = max(markf.values()) if len(markf) != 0 else 0
    if dotnum >= 3 or numnum >= 2:
        #paralell scores
        secparascore = SCORE['PARA_SENTENCE']*(dotnum+numnum)
        section.scores[ImageScore.TABLE] += secparascore
    

def readsections(filename):
    #textfile:unicode
    try:
        with codecs.open(filename,u"r",u"utf-8-sig") as file:
            rawtext = unicode(file.read())
    except IOError as e:
        logger.error(u"in:"+e.filename)
        logger.error(e)
        raise

    #normalize text 
    normal_text = text_normalizer(rawtext)

    #RawText:unicode:list(sptext?unicode)
    sections = split_sections(normal_text)
    return sections

def sectionscoring(sections,filename=None):
    """sections:list(sentence:SpText)"""

    logger.debug(u"section#:%d start%s"
                    %(len(sections.childs),
                      (u" in "+filename) if filename != None else u"")
    )

    allpara = {}
    sectionlength = len(sections.childs)

    for section in sections.childs:

        logmessage = u"in section:%2d/%2d"%\
            (sections.childs.index(section)+1,sectionlength)
        if filename:
            logmessage += u" in "+filename
        logger.debug(logmessage)

        #Section(sptext?unicode):list(sptext?unicode)
        sentences = split_sentences(section)
        section.childs = sentences
        section.para_words = []
        section.descriptions = []
        section.morphs = []
        section.cluewords = []
        #scoring
        section.scores = dict.fromkeys(TAGLIST,0.0) #score[tagname] -> score

        #Section Paralells
        get_section_paralells(section)

        for sentence in sentences:
            #*has Paralell?
            paras = get_paralell(sentence)
            if len(paras) > 0:
                section.para_words.extend(paras)
                wordset = reduce(lambda a,b:a+b,[b[0].keys() for b in paras])
                for word in wordset:
                    if word.word in allpara:
                        allpara[word.word].append(section)
                    else:
                        allpara[word.word] = [section]
                for para in paras:
                    #is about numerical? sentential? or example?
                    desc_bunsetsus = reduce(lambda a,b:a+b,para[0].values())
                    if not len(desc_bunsetsus) > 0:
                        section.scores[ImageScore.IMAGE] += SCORE['PARA_IMAGE']*len(para[0])
                    else:
                        if is_numerical(para):
                            section.scores[ImageScore.GRAPH] += SCORE['PARA_GRAPH']*len(para[0])
                        else:
                            section.scores[ImageScore.TABLE] += SCORE['PARA_TABLE']*len(para[0])

            #*is Description about paralell word?
            for para in allpara:
                if has_description(sentence.childs,para)\
                        or re.match(para,sentence.childs[0].word if len(sentence.childs) > 0 else u""):
                    section.descriptions.append((para,sentence))
                    section.scores[ImageScore.TABLE] += SCORE['DESC_SENT']
                    for sec in allpara[para]:
                        if not sec == section:
                            sec.descriptions.append((para,sentence))
                            sec.scores[ImageScore.TABLE] += SCORE['DESC_WORD']
        
        #*has ClueWord and/or keyExp?
        clueword_scores = scoring_clueword(section)
        if len(clueword_scores) == 0:
            logger.error('no-clueword in '+filename)
        for clueword_score in clueword_scores:
            section.cluewords.append(clueword_score[0])
            for key in ImageScore.taglist:
                section.scores[key] += clueword_score[1].dict[key]

        #sum score and set in Section
        section.score = 0.0
    for section in sections:
        for soloscore in section.scores.values():
            section.score += soloscore
    return sections


def writescore(sections,filename):
    #sort Sections by score
    sorted_section = sorted(sections.childs,key=lambda section:section.score,reverse=True)

    with codecs.open(filename,u"w",encoding=u"utf-8-sig")\
    as answerfile:
        stflag = True
        for section in sorted_section:
            if stflag:
                stflag = False
            else:
                answerfile.write(u"\n")
            answerfile.write(u"In Section %d, Score:%f"%(section.No,section.score)+u"\n")
            answerfile.write(section.text+u"\n")
            answerfile.write(u"paraword\n")
            for paraitem in section.para_words:
                answerfile.write(u"list\n")
                if any(map(lambda a:len(a) > 0,paraitem[0].itervalues())):
                    for item in paraitem[0].iteritems():
                        answerfile.write(item[0].word + u":")
                        wordlist = [s.word for s in item[1]]
                        answerfile.write(",".join(wordlist) + u"\n")
                else:
                    answerfile.write(u"  [" + u", ".join([p.word for p in paraitem[0]]) + u"]\n")
                answerfile.write(u"to root\n")
                answerfile.write(u"  [" + u", ".join([p.word for p in paraitem[1]]) + u"]\n")
                answerfile.write(u"to reaf\n")
                answerfile.write(u"  [" + u", ".join([p.word for p in paraitem[2]]) + u"]\n")
            for descitem in section.descriptions:
                answerfile.write(u"description : "+descitem[0]+u"\n")
                answerfile.write(u"\t : "+descitem[1].text+u"\n")
            answerfile.write(u"clueword:\n")
            if len(section.cluewords) > 0:
                answerfile.write(u", ".join(section.cluewords)+u"\n")
            for key in ImageScore.taglist:
                answerfile.write(key+u" : "+unicode(section.scores[key])+u"\n")

def filescoring(fromfilename,tofilename):
    readfile_name = fromfilename
    answerfilen_name = tofilename
    logger.debug(u"from:"+fromfilename+u", to:"+tofilename)
    sections = readsections(readfile_name)

    anssections = sectionscoring(sections,filename=readfile_name)

    logger.debug(u"write answer to %s"%(answerfilen_name))
    #show answer and...
    writescore(anssections,answerfilen_name)

    logger.debug(u"file:%s is end."%readfile_name)
    # F I N I S H ! ( O S H I M A I ! )

if __name__==u"__main__":
    MAXTHREAD = 8
    #p = Pool(MAXTHREAD)
    for dir in os.listdir(u"datas"):
        if not u"-answer" in dir:
            filename,exe = os.path.splitext(dir)
            inputfilename = os.path.join(ur"datas\\",filename+exe)
            outputfilename = os.path.join(ur"datas\\",filename+u"-answer"+exe)
            #p.apply_async(func=filescoring,
            #              args=(inputfilename,outputfilename),
            #)
            #section_scoring(inputfilename,outputfilename)
    #p.close()
    #p.join()
    filescoring(u"sample.txt",u"sample-ans.txt")