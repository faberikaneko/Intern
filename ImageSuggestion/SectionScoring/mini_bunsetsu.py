# -*- encoding:utf-8 -*-
import regex as re

def get_root(mini):
    """ get minibunsetsu root """
    while mini.parent:
        mini = mini.parent
    return mini

class MiniBunsetsu:
    def __init__(self,id,word,parent = None):
        self.id = id
        self.word = word
        self.parent = parent
        self.childList = []
        self.tag = {}
    def isparalell(self):
        return self.tag.get(u"depend") == (u"P" or u"A")\
                and self.tag.get(u"体言")
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

    def __getattr__(self,name):
        if name in self.tag:
            return self.tag.get(name)
        else:
            raise AttributeError

    def description_about(self,word):
        if self.tag.get(u"ハ") and re.match(self.word,word):
            return True
        else:
            return False