# coding: utf-8

import re
import os
import threading
from HTMLParser import HTMLParser
import random

class MyHTMLParser(HTMLParser):

    altList = [ ]
    hrefList = [ ]

    imgCount = 0
    hrefCount = 0

    startHTTP = re.compile(r'http://')
    startHTTPS = re.compile(r'https://')
    jpgHTTP = re.compile(r'.jpg')
    gifHTTP = re.compile(r'.gif')
    pngHTTP = re.compile(r'.png')
    bmpHTTP = re.compile(r'.bmp')

    count = 5

    global_lock = threading.Lock()

    def __init__(self):
        HTMLParser.__init__(self)

    def delFiles(self):
        if os.path.exists('./altList.txt'):
            os.remove('./altList.txt')
        if os.path.exists('./hrefList.txt'):
            os.remove('./hrefList.txt')

    def openFiles(self):
        self.falt = open('./altList.txt','at')
        self.fhref = open('./hrefList.txt','at')

    def closeFiles(self):
        self.falt.close()
        self.fhref.close()

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'img':
            for i in attrs:
                if i[0].lower() == 'alt':
                    alt = re.sub(ur"[^\p{Alphabetic}]",'',i[1])
                    if alt!="":
                        self.global_lock.acquire()
                        self.imgCount += 1
#                        self.altList.append(i[1].encode('utf-8'))
                        try:
                            self.falt.write(str(self.imgCount) + " : " + i[1].encode('utf-8') + '\n')
                            print "HIT"
                        except UnicodeDecodeError as e:
                           print "ERROR : " + str(e.reason)
                        self.global_lock.release()

        if tag.lower() == 'a':
            for i in attrs:
                if i[0].lower() == 'href':
                    if i[1]!="":
                        if (self.startHTTP.match(i[1].decode('utf-8'))!=None) or (self.startHTTPS.match(i[1].decode('utf-8'))!=None):
                            if (self.jpgHTTP.findall(i[1].decode('utf-8'))!=None)or(self.gifHTTP.findall(i[1].decode('utf-8'))!=None)or(self.pngHTTP.findall(i[1].decode('utf-8'))!=None)or(self.bmpHTTP.findall(i[1].decode('utf-8'))!=None):
                                if self.hrefCount < self.count:
                                    if random.randint(1,5)%2 == 0:
                                        if i[1]!="":
                                            self.global_lock.acquire()
#                                            self.hrefList.append(i[1].encode('utf-8'))
                                            try:
                                                self.fhref.write(i[1].encode('utf-8') + '\n')
                                            except UnicodeDecodeError as e:
                                                print "ERROR : " + str(e.reason)
                                            self.hrefCount += 1
                                            self.global_lock.release()
    
    def returnAltList(self):
        return self.altList
        

    def returnHrefList(self):     
        return self.hrefList

    def resetList(self):
        self.hrefList = []
        self.altList = []
