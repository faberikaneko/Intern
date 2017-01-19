# coding: utf-8

import urllib2
import sys
import re
from MyHTMLParser import MyHTMLParser
from KeyClass import KeyClass
from Queue import Queue
import threading
import ssl
import time
import codecs


class MainClass(threading.Thread):
    
    request = [ ]

    ssl._create_default_https_context = ssl._create_unverified_context

    def __init__(self):

        print "Init"

        reload(sys)
        sys.setdefaultencoding('utf-8')

    def checkUrl(self,url):

        try:
            urllib2.urlopen(urllib2.Request(url))
            self.request.append(urllib2.Request(url))
        except urllib2.URLError as e:
            print "ERROR : " + str(e.reason)
            
    
    def pickAltAndHref(self):

        print "getHtml"
        for req in main.request:
            self.htmlText = urllib2.urlopen(req)
            self.parser.hrefCount = 0
            try:
                self.parser.feed(self.htmlText.read())
            except AssertionError as e:
                print "AssertionError : " + str(e.reason)

    def thre(self,req):
        self.htmlText = urllib2.urlopen(req)
        self.parser.hrefCount = 0
        self.parser.feed(self.htmlText.read())
 #       main.pickAltAndHref()
#        print "END thre "

    def openImputUrl(self,filename):
        buf = Queue()
        text = self.readfile(filename)
        lines = text.split('\n')
        for url in lines:
            print str(url)
            buf.put(str(url))
        return buf       

    def readfile(self,imputfilename):
        """read imput file from imputfilename(file) to rawText"""
        try:
            ans = codecs.open(imputfilename,"r",encoding="utf-8-sig").read()
        except UnicodeDecodeError:
            ans = codecs.open(imputfilename,"r",encoding="shift-jis").read()
        
        return ans


if __name__ == "__main__":
    
    main = MainClass()

    imputUrl = Queue()
    imputUrl = main.openImputUrl('./imputUrls.txt')
    
    main.parser = MyHTMLParser()
    main.parser.delFiles()
    main.parser.openFiles()
    for j in range(0,2):
        for i in range(0,imputUrl.qsize()):
            print "----------------------------------------------START " + str(i) + " ----------------------------------------------"
            print "----------------------------------------------START " + str(i) + " ----------------------------------------------"
            print "----------------------------------------------START " + str(i) + " ----------------------------------------------"
            for j in range(0,imputUrl.qsize()):
                url = imputUrl.get()
                main.th1 = threading.Thread(target=main.checkUrl, args=(url,))
                main.th1.setDaemon(True)
                main.th1.start()
            main.th1.join()
            print "th 1 JOIN!!!"

            while main.th1.isAlive():
                time.sleep(100)
        
            print "request : " + str(len(main.request))


            for req in main.request:
                main.th2 = threading.Thread(target=main.thre, args=(req,))
                main.th2.setDaemon(True)
                main.th2.start()
            main.th2.join()
            print "th2 JOIN!!!"

            while main.th2.isAlive():
                time.sleep(100)

        imputUrl = main.openImputUrl('./hrefList.txt')

        main.parser.closeFiles()


        keyClass = KeyClass()
    
        rawText = keyClass.readfile('./altList.txt')

        keys = keyClass.keitaiso(rawText)

#        main.parser.openFiles()
        
            #main.hrefList = main.parser.returnHrefList()

            #for href in main.hrefList:
            #    imputUrl.put(href)
            #print href

            #main.parser.resetList() 

            

        
    
    
    #TODO : 1要素ごとにけいたいそかいせき　

    

    