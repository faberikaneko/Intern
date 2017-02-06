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

PARA_GRAPH_SCORE = 1
PARA_TABLE_SCORE = 1
DESCRIPTION_SCORE = 1
TAGLIST = [
    u"table",u"picture",u"graph",u"flow"
]

class MyHTMLparser(HTMLParser):
    def __init__(self):
        self.datalist = []
        self.tagstack = []
        return HTMLParser.__init__(self)
    def handle_data(self,data):
        if len(self.tagstack) > 0 and self.tagstack[-1] == u"p" or u"div":
            self.datalist.append(data)
    def handle_starttag(self, tag, attrs):
        self.tagstack.append(tag)
    def handle_endtag(self, tag):
        while self.tagstack.pop() != tag:
            pass

def html2text(parsedhtml):
    """parsedhtml: unicode -> text: unicode"""
    print(u"get raw text")
    #If you want, do Unicode Nomalize
    #unicodedata.nomalize(parsedhtml)

    #How?
    return re.sub(ur"<.*?>","",parsedhtml)

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
    """maybe use ScoringClass"""
    ans = dict.fromkeys(TAGLIST,0.0)
    #sum score
    for clueword in {u"para":{u"table":0.0,u"picture":1.0,u"graph":0.0,u"flow":0.0}}.items():
        if text.find(clueword[0]) >= 0:
            for key in clueword[1]:
                ans[key] += clueword[1][key]
    return ans

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

    for section in sections:
        #Section(sptext?unicode):list(sptext?unicode)
        sentences = split_sentences(section)
        section.paralells = []
        section.descriptions = []

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
            clueword_score = scoring_clueword(sentence.text)
            for key in scores:
                scores[key] += clueword_score[key]

            #*is Description about paralell word?
            for para in allpara:
                if has_description(sentence.childs,para):
                    print("It is description about:"+para)
                    section.descriptions.append(para)
                    scores[u"table"] += DESCRIPTION_SCORE

        #sum score and set in Section
        section.scores = scores
        section.score = float(reduce(lambda a,b:a+b,scores.values()))

    #sort Sections by score
    sorted_section = sorted(sections,key=lambda section:section.score,reverse=True)

    #show answer and...
    with codecs.open(answerfilen_name,u"w",encoding=u"utf-8-sig")\
    as answerfile:
        stflag = True
        for section in sorted_section:
            if stflag:
                stflag = False
            else:
                print(u"\n")
                answerfile.write(u"\n")
            print(u"In Section %d, Score:%f"%(section.No,section.score))
            print(section.text)
            answerfile.write(u"In Section %d, Score:%f"%(section.No,section.score)+u"\n")
            answerfile.write(section.text+u"\n")
            for paraitem in section.paralells:
                print(u",".join(paraitem)+u"\n")
                answerfile.write(",".join(paraitem)+u"\n")
            for descitem in section.descriptions:
                print(u"description : "+descitem+u"\n")
                answerfile.write(u"description : "+descitem+u"\n")
            for item in section.scores.items():
                print(item[0] +u":"+ unicode(item[1]))
                answerfile.write(item[0]+u" : "+unicode(item[1])+u"\n")

    # F I N I S H ! ( O S H I M A I ! )

if __name__==u"__main__":
    threads = []
    for dir in os.listdir(u"datas"):
        if not u"-answer" in dir:
            filename,exe = os.path.splitext(dir)
            inputfilename = os.path.join(ur"datas\\",filename+exe)
            outputfilename = os.path.join(ur"datas\\",filename+u"-answer"+exe)
            t = threading.Thread(
                target=section_scoring,
                args=(inputfilename,outputfilename)
            )
            t.setDaemon(True)
            t.start()
            threads.append(t)

    for t in threads:
        t.join()
    print("end")