import re
import codecs 

text = ""
with codecs.open("after.txt",mode="r",encoding="utf-8-sig") as file:
    text = file.read()
count=0
maxcount = 20
flaglist = re.split("\r\n(?=Flag)",text)
writelist = []
s = ""
for flagnode in flaglist:
    s += flagnode+"\r\n"
    count += 1
    if count >= maxcount:
        writelist.append(s)
        s = ""
        count = 0
writelist.append(s)
for index,writenode in enumerate(writelist):
    print(writenode)
    with codecs.open("afters-"+str(index)+".txt",mode="w",encoding="utf-8-sig") as file:
        file.write(writenode)
