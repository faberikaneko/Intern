# coding: utf-8

import urllib2
import sys
import re
from MyHTMLParser import MyHTMLParser
from Queue import Queue
import threading
import ssl
import time


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
        print "END thre "



if __name__ == "__main__":
    imputUrl = Queue()
    imputUrl.put(u'http://viral-community.com/blog/google-analytics-cv-7693/')
    main = MainClass()
    main.parser = MyHTMLParser()
    main.parser.delFiles()
    main.parser.openFiles()

    for i in range(0,5):
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
        main.th2.join(1000)
        print "th2 JOIN!!!"

        while main.th2.isAlive():
            time.sleep(100)
        
    
        main.hrefList = main.parser.returnHrefList()

        for href in main.hrefList:
            imputUrl.put(href)
        print href

        main.parser.resetList() 


    print "haha"
#    main.parser.closeFiles()

    