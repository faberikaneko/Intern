# coding: utf-8

import codecs
import MeCab
import regex as re

class KeyClass():
    """description of class"""

    
    
    def readfile(self,imputfilename):
        """read imput file from imputfilename(file) to rawText"""
        try:
            ans = codecs.open(imputfilename,"r",encoding="utf-8-sig").read()
        except UnicodeDecodeError:
            ans = codecs.open(imputfilename,"r",encoding="shift-jis").read()
        
        return ans

    def keitaiso(self,rawText):

        lines = rawText.split('\n')
        keyList = []
        import os
        import io
        if os.path.exists('./keyList.txt'):
            fkey = io.open('./keyList.txt','rt',encoding="utf-8-sig")
            keyLine = fkey.readlines()
            for key in keyLine:
                keyList.append(key.strip())
            fkey.close()

        m = MeCab.Tagger("-Owakati")
        for line in lines:
            if line != "":
                text = re.sub(ur"[^\p{Alphabetic}]",'',line.split(': ')[1])
#                print text
                node = m.parseToNode(text.encode('utf-8'))
                while node.next:
                    pos = node.feature.split(',')[0]
                    key = node.surface
                    s = str('名詞')
                    if pos == s and len(key) > 1:
                        keyList.append(key.decode('utf-8'))
                    node = node.next
        keySet = set(keyList)

        fkey = open('./keyList.txt','w')

        for word in keySet:
            word =  re.sub(ur"[^\p{Alphabetic}]",'',word)
            print word
            if word!="":
                fkey.write(word.encode('utf-8') + '\n')

        fkey.close()

