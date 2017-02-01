#   encoding:utf-8

import sys
import os
import codecs
from pyknp import KNP

import regex as re

from janome.tokenizer import Tokenizer

knp = None

def selectNorm(fstring):
    """ 正規化代表表記を抽出します
    """
    begin = fstring.find(ur'正規化代表表記:')
    end = fstring.find(ur'>', begin + 1)
    return fstring[begin + len(ur'正規化代表表記:') : end]

def is_noun(fstring):
    """ return True if it is noun, else return false."""
    return not re.search(ur"体言",fstring) == None

def select_dependency_structure(line):
    """係り受け構造を抽出します
    """

    # KNP
    #knp = KNP(option = u"-tab")
    global knp
    if knp == None:
        knp = KNP(option = '-tab -anaphora')

    # 解析
    #escape
    escapelist = [
        #url escape
        (ur"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+",u"(urls)"),
        #blanket escape
        (ur"<",ur"＜"),
        (ur">",ur"＞"),
        #coron escape
        (ur":",ur"："),
        #cdot escape
        (u'•|·|･','・'),
        #dot and comma
        (u",",u"，"),
        (u"\.",u"．"),
        (u"/",u"／")
    ]

    for escape in escapelist:
        line = re.sub(escape[0],escape[1],line)

    #kaiseki
    result = knp.parse(line)

    # 文節リスト
    bnst_list = result.bnst_list()
    miniList = {}
    index = 0
    for bnst in bnst_list:
        id = bnst.bnst_id
        norm = selectNorm(bnst.fstring)
        mini = MiniBunsetsu(id,norm)
        mini.tag = mini.fstring_to_tag(bnst.fstring)
        mini.tag[u"depend"] = unicode(bnst.dpndtype)
        miniList[id] = mini

    for bnst in bnst_list:
        for cbnst in bnst.children:
            cmini = miniList[cbnst.bnst_id]
            miniList[bnst.bnst_id].childList.append(miniList[cbnst.bnst_id])
        if bnst.parent != None:
            #部分並列は係り先を変更しておく
            if miniList[bnst.bnst_id].tag.get(u"depend") == u"I":
                miniList[bnst.bnst_id].parent = miniList[bnst.bnst_id + 1]
            else:
                miniList[bnst.bnst_id].parent = miniList[bnst.parent.bnst_id]
    return miniList

def get_root(mini):
    """ get minibunsetsu root """
    while mini.parent:
        mini = mini.parent
    return mini

def miniListToTexts(miniList):
    anslist = {}
    for mini in miniList.itervalues():
        if mini.isparalell():
            childName = unicode(mini.id) + u":"+ mini.word
            parentName = unicode(mini.parent.id) +u":" + mini.parent.word
            anslist[childName] = parentName
    return anslist

class MiniBunsetsu:
    def __init__(self,id,word,parent = None):
        self.id = id
        self.word = word
        self.parent = parent
        self.childList = []
        self.tag = {}
    def isparalell(self):
        return self.tag.get(u"depend") == (u"P" or u"A") and self.tag.get(u"体言")
    def __str__(self):
        return self.word

    def fstring_to_tag(self,fstring):
        """fstring:unicode -> tags:dict(unicode:unicode,bool)"""
        ans = {}
        tagstre = re.compile(ur"<(.*?)>")
        keystre = re.compile(ur"(?P<key>.*):(?P<data>.*)")
        for tagst in tagstre.findall(fstring):
            mat = keystre.match(tagst)
            if mat:
                ans[mat.group(ur"key")] = mat.group(ur"data")
            else:
                ans[tagst] = True
        return ans
    def getallchilds(self):
        l = []
        for child in self.childList:
            l.extend(child.getallchilds())
        l.extend(self.childList)

        return l

def parseSentences(section):#->sectionlist
    answerlist = []
    st = section.text.strip()
    for line in st.split(u"\n"):
        sentenceRe = re.compile(ur"(?P<all>(?:[^]{「《【『［〈≪（＜｛{()}｝＞）≫〉］』】》」。]*(?P<rec>[[「《【『［〈≪（＜｛[{(](?:[^]{「《【『［〈≪（＜｛{()}｝＞）≫〉］』】》」]*|(?P&rec))*[])}｝＞）≫〉］』】》」]))*.*?(。|\Z))")
        sentencelist = [text(i[0]) for i in sentenceRe.findall(line.strip())]
        sentencelist = filter(lambda s:len(s.text) > 0,sentencelist)
        answerlist.extend(sentencelist if len(sentencelist) else [text(line.strip())])
    return answerlist

class text(object):
    def __init__(self,text,childs = None):
        if not isinstance(text,unicode):
            raise ValueError(text + " is not unicode")
        self.text = text
        self._childs = childs if childs != None else []
        return
    def __str__(self):
        return self.text
    def __getitem__(self,key):
        try:
            return self._childs[key]
        except:
            raise
    def setchilds(self,childs):
        self._childs = childs
    def getchilds(self):
        return self._childs

def dictLooper(minidict):
    #[key] -> list(key)
    answer = {}
    already = set()
    for key in minidict:
        if not key in already:
            if minidict[key] in answer:
                answer[key] = [key] + answer[minidict[key]]
                answer.pop(minidict[key])
                already.add(key)
            else:
                con = key
                answer[key] = [key]
                while con in minidict:
                    answer[key] += [minidict[con]]
                    already.add(con)
                    con = minidict[con]
    return answer


if __name__ == '__main__' :
    #set stdio encoding
    reload(sys)
    sys.setdefaultencoding("utf-8")
    sys.stdin = codecs.getreader("utf-8")(sys.stdin)
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

    if not os.path.exists(ur".\output"):
        os.mkdir("./output")
    filenamelist = os.listdir(ur".\input")

    for filename in filenamelist:
        inputFileName = os.path.join(ur".\input",filename)
        outputFileName = os.path.join(ur".\output",filename)

        #has done?
        if os.path.exists(outputFileName):
            print(inputFileName + " has already done.")
            continue

        #read file into lines
        lines = []
        print(u"readfile from:"+inputFileName)
        try:
            with codecs.open(inputFileName,"r","utf-8-sig") as file:
                lines = [l.strip() for l in file.readlines()]
        except IOError:
            print("no such file.")
            raise
            if not len(lines) > 0:
                print("no input file")

        with codecs.open(outputFileName,"w","utf-8-sig") as file:
            pass

        print(u"split texts"),
        #line in lines marge into sections
        sections = []
        s = u""
        hSpace = re.compile(" ")
        for line in lines:
            if len(line) == 0:
                if not s ==u"":
                    sections.append(text(hSpace.sub(u"",s)))
                s = u""
            else:
                s += line + u"\n"
        sections.append(text(s))
        print(u":"+unicode(len(sections)))

        print(u"split sections")
        #section in sections parse to sentence
        #and put into section.child
        for section in sections:
            sentences = parseSentences(section)
            section.setchilds(sentences)

        print(u"do read")
        #cdot paralell
        output_texts = []
        cdot = re.compile(ur"・")
        firstFlag = True
        for section in sections:
            print(u"in:"+unicode(sections.index(section)))
            if firstFlag:
                firstFlag = False
            else:
                output_texts.append(u"\n")
            output_texts.append("Section:\n")
            has_cdots = filter(lambda s:cdot.match(s.text.strip()),section)
            if len(has_cdots) > 1:
                output_texts.append(section.text)
                #cdot paralell section
                output_texts.append("\tPara:\n")
                for has_cdot in has_cdots:
                    output_texts.append(u"\t"+unicode(has_cdot)+u"\n")
            else:
                #inner paralell section
            
                #sentence (in sentences in sections) parse to miniBunsetsu
                #and put into sentence.child
                for sentence in section:
                    miniList = {}
                    try:
                        miniList = select_dependency_structure(sentence.text)
                    except Exception as e:
                        print(e.message)
                        raise
                    sentence.setchilds(miniList)

                for sentence in section:
                    output_texts.append(sentence.text+u"\n")

                    #list make to paralell list
                    paralist = []
                    miniList = sentence.getchilds()
                    already = set()
                    for item in miniList.iteritems():
                        if item[1] in already:
                            continue
                        id = item[0]
                        mini = item[1]
                        if mini.isparalell():
                            plist = {}
                            cur = mini
                            while cur != None and cur.isparalell():
                                plist[cur] = []
                                already.add(cur)
                                cur = cur.parent
                            for pc in plist:
                                for ps in pc.getallchilds():
                                    if not ps in plist:
                                        plist.get(pc).append(ps)
                            plist[cur] = []
                            for ps in cur.getallchilds():
                                if ps.id > id and not ps in plist:
                                    plist[cur].append(ps)
                            proot = cur
                                
                            toroot = []
                            cur = proot.parent
                            while cur != None:
                                toroot.append(cur)
                                cur = cur.parent

                            allchild = []
                            if len(plist[mini]) > 0:
                                id = min([i.id for i in plist[mini]])
                            for ps in proot.getallchilds():
                                if ps.id <id:
                                    allchild.append(ps)
                            paralist.append((plist,toroot,allchild))
                    for paraitem in paralist:
                        output_texts.append(u"list\n")
                        if any(map(lambda a:len(a) > 0,paraitem[0].itervalues())):
                            for item in paraitem[0].iteritems():
                                output_texts.append(item[0].word + u":")
                                wordlist = [s.word for s in item[1]]
                                output_texts.append(",".join(wordlist) + u"\n")
                        else:
                            output_texts.append(u"  [" + u", ".join([p.word for p in paraitem[0]]) + u"]\n")
                        output_texts.append(u"to root\n")
                        output_texts.append(u"  [" + u", ".join([p.word for p in paraitem[1]]) + u"]\n")
                        output_texts.append(u"to reaf\n")
                        output_texts.append(u"  [" + u", ".join([p.word for p in paraitem[2]]) + u"]\n")

            with codecs.open(outputFileName,"a","utf-8-sig") as file:
                file.writelines(output_texts)
            output_texts = []