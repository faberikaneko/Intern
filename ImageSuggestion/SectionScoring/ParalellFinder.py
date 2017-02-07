#   encoding:utf-8

import sys
import os
import codecs
from pyknp import KNP

import regex as re

from sptext import SpText
from mini_bunsetsu import MiniBunsetsu

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
    #global knp
    #if knp == None:
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
    miniList = [None]*len(bnst_list)
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

def parse_sections(textlist):
    #line in lines marge into sections
    sections = []
    s = u""
    hSpace = re.compile(" ")
    for line in textlist:
        if len(line) == 0:
            if not s ==u"":
                sections.append(SpText(hSpace.sub(u"",s)))
            s = u""
        else:
            s += line + u"\n"
    sections.append(SpText(s))
    return sections

def parse_sentences(section):#->sectionlist
    answerlist = []
    st = section.text.strip()
    for line in st.split(u"\n"):
        sentenceRe = re.compile(ur"(?P<all>(?:[^]{「《【『［〈≪（＜｛{()}｝＞）≫〉］』】》」。]*(?P<rec>[[「《【『［〈≪（＜｛[{(](?:[^]{「《【『［〈≪（＜｛{()}｝＞）≫〉］』】》」]*|(?P&rec))*[])}｝＞）≫〉］』】》」]))*.*?(。|\Z))")
        sentencelist = [SpText(i[0]) for i in sentenceRe.findall(line.strip())]
        sentencelist = filter(lambda s:len(s.text) > 0,sentencelist)
        answerlist.extend(sentencelist if len(sentencelist) else [SpText(line.strip())])
    return answerlist

def sentence_paralell_finder(sentence):
    try:
        miniList = select_dependency_structure(sentence.text)
    except Exception as e:
        logging.debug(e.message)
        raise
    sentence.childs = miniList

    #list make to paralell list
    paralist = []
    miniList = sentence.childs
    already = set()
    for item in miniList:
        if item in already:
            continue
        id = miniList.index(item)
        mini = item
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
    return paralist

def sentence_paralell_writer(sentence,file):
    file.write(sentence.text+u"\n")
    paralist = sentence_paralell_finder(sentence)
    for paraitem in paralist:
        file.write(u"list\n")
        if any(map(lambda a:len(a) > 0,paraitem[0].itervalues())):
            for item in paraitem[0].iteritems():
                file.write(item[0].word + u":")
                wordlist = [s.word for s in item[1]]
                file.write(",".join(wordlist) + u"\n")
        else:
            file.write(u"  [" + u", ".join([p.word for p in paraitem[0]]) + u"]\n")
        file.write(u"to root\n")
        file.write(u"  [" + u", ".join([p.word for p in paraitem[1]]) + u"]\n")
        file.write(u"to reaf\n")
        file.write(u"  [" + u", ".join([p.word for p in paraitem[2]]) + u"]\n")

def work(filename):
    inname = os.path.join(ur".\input",filename)
    outname = os.path.join(ur".\output",filename)
    #If output has already done:
    if os.path.exists(outname):
        logging.debug(inname + " is already done.")
        return
    logging.debug("start "+outname)

    #read file into inlines
    inlines = []
    with codecs.open(inname,mode="r",encoding="utf-8-sig") as file:
        inlines = [s.strip() for s in file.readlines()]
        if len(inlines) == 0:
            return
    
    #parse and split
    sections = parse_sections(inlines)
    for section in sections:
        section.childs = parse_sentences(section)

    with codecs.open(outname,mode="w",encoding="utf-8-sig") as file:
        firstFlag = True
        for section in sections:
            if firstFlag:
                firstFlag = False
            else:
                file.write(u"\n")
            file.write("Section:\n")
            has_cdots = filter(lambda s:s.text.strip().find(u"・") == 0,section)
            if len(has_cdots) > 1:
                file.write(section.text)
                #cdot paralell section
                file.write("\tPara:\n")
                for has_cdot in has_cdots:
                    file.write(u"\t"+unicode(has_cdot)+u"\n")
            else:
                #inner paralell section
            
                #sentence (in sentences in sections) parse to miniBunsetsu
                #and put into sentence.child
                tlist = []
                for sentence in section:
                    t = threading.Thread(\
                        target=sentence_paralell_writer,\
                        args=(sentence,file)\
                    )
                    t.setDaemon(True)
                    t.start()
                    tlist.append(t)
                for t in tlist:
                    t.join()
    logging.debug(outname + "is finish.")
    return

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
        t = threading.Thread(target=work,args=(filename,))
        t.setDaemon(True)
        t.start()
    this = threading.current_thread()    
    for t in threading.enumerate():
        if t is this:
            continue
        logging.debug('joining %s', t.getName())
        t.join()