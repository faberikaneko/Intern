# coding: utf-8

from HTMLParser import HTMLParser
import urllib2

class SectionPickUpClass(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.section_flag = False
        self.fout = open('./output.txt','w')

    def checkUrl(self,url):
        try:
            result = urllib2.urlopen(urllib2.Request(url))
        except urllib2.URLError as e:
            print "ERROR : " + str(e.reason)

        return result

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'p':
            for i in attrs:
                if i[0].lower() == 'class':
                    if i[1]=='text':
                        self.section_flag = True

    def handle_data(self, data):
        if self.section_flag:
            self.fout.write(data.encode('utf-8') + '\n')
            self.section_flag = False


if __name__=='__main__':
    main = SectionPickUpClass()
    imputUrl = u'https://careerpark.jp/76647'

    htmlText = main.checkUrl(imputUrl)

    main.feed(htmlText.read().decode('utf-8'))
