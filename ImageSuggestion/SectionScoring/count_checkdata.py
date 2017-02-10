import regex as re
import os
import codecs

def count_checkdata(dirname):
    alls = 0
    point = 0
    ma = re.compile(" check is (?<point>.*) / (?<all>.*)")
    for dir in os.listdir(dirname):
        if u"-checker" in dir:
            with codecs.open(dirname+"\\\\"+dir,mode="r",encoding="utf-8-sig") as file:
                matchobj = ma.match(file.readlines()[-1])
                alls += int(matchobj.group("all"))
                point += int(matchobj.group("point"))
    print("check is %d / %d"%(point,alls))
    return point,alls

if __name__ == "__main__":
    count_checkdata(u"docs\\21_40")
