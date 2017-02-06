# -*- encoding:utf-8-sig -*-

import sys
import codecs
import regex as re
import unicodedata
from sptext import SpText

PARA_GRAPH_SCORE = 1
PARA_TABLE_SCORE = 1
DESCRIPTION_SCORE = 1
TAGLIST = [
    u"table",u"picture",u"graph",u"flow"
]

def parseHTML(htmltext):
    """html: unicode -> parsedHTML: type is not determined"""
    print(u"parse html")
    #lxml? BeautifulSoup? HTMLparser? You can use you want.
    #htmlparser = HTMLParser()
    #parsedhtml = htmlparser.feed(htmltext)
    ans = u""
    body = re.search(ur"<body.*?>(?<body>(?:.|\n|\r)*)</body>",htmltext,
                     flags=re.IGNORECASE|re.MULTILINE)
    if body:
        pstrs = re.findall(ur"<p>(.*)</p>",body.group("body"),
                           flags=re.IGNORECASE|re.MULTILINE)
        for pstr in pstrs:
            ans += pstr + u"\n"
    return ans[:-1]

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
    #., -> ，．(without number point)
    #<>[]{} ()-> ＜＞［］｛｝（）
    #!"#$%&'=~|?_-^\/;:+*
    # -> ！”＃＄％＆’＝～｜？＿‐￥・／；：＋＊
    replace_halfres = [
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
    for line in re.split(ur"\n{2,}",text):
        sections.append(SpText(line))
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
    """sentence: unicode -> list[list[unicode]]?"""

    #maybe use Paralell Finder
    return [text.split()]

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

def scoring_keyexp(text):
    """maybe use ScoringClass"""
    ans = dict.fromkeys(TAGLIST,0.0)
    #sum score
    return ans

def is_description(text,word):
    """text: list[bunsetsu], word: unicode -> bool
        return True if text descript about word."""
    if text.find(word) >= 0:
        return True
    return False

def section_scoring(fromfilename,tofilename):
    #HTMLFile:unicode
    htmlfile_name = fromfilename
    answerfilen_name = tofilename
    try:
        with codecs.open(htmlfile_name,u"r",u"utf-8-sig") as htmlfile:
            htmltext = unicode(htmlfile.read())
    except IOError as e:
        print(u"in:"+e.filename)
        print(e)
        raise

    #HTMLText:unicode:unicode (and more?)
    parsedhtml = parseHTML(htmltext)
    rawtext = html2text(parsedhtml)

    #normalize text 
    normal_text = text_normalizer(rawtext)

    #RawText:unicode:list(sptext?unicode)
    sections = split_sections(normal_text)

    for section in sections:
        #Section(sptext?unicode):list(sptext?unicode)
        sentences = split_sentences(section)

        #scoring
        scores = dict.fromkeys(TAGLIST,0.0) #score[tagname] -> score
        allpara = set()
        for sentence in sentences:
            #*has Paralell?
            paras = get_paralell(sentence.text)
            if len(paras) > 0:
                allpara = allpara.union(set(reduce(lambda a,b:a+b,paras)))
                for para in paras:
                    #is about numerical? or sentential?
                    if is_numerical(para):
                        scores[u"graph"] += PARA_GRAPH_SCORE
                    else:
                        scores[u"table"] += PARA_TABLE_SCORE

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
            print(u"Score:" + unicode(section.score))
            print(section.text)
            answerfile.write(u"Score:" + unicode(section.score))
            answerfile.write(section.text)
            for item in section.scores.items():
                print(item[0] +u":"+ unicode(item[1]))
                answerfile.write(item[0]+u" : "+unicode(item[1]))

    # F I N I S H ! ( O S H I M A I ! )



if __name__==u"__main__":
    section_scoring(u"sample.html",u"answer.txt")