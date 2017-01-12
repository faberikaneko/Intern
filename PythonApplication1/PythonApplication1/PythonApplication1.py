#coding:utf-8

import MeCab
import sys
import codecs

import csv

m = MeCab.Tagger("-Owakati")

f1 = open("hoge.txt","r")
t = f1.read().decode("utf-8")
f1.close()
f2 = open("huga.txt","w")
f2.write(m.parse(t.encode("utf-8")))
f2.close()

data = []

with open("ClueWord_List.csv","rb") as f:
	reader = csv.DictReader(f)
	for row in reader:
		data.append(row)

keyword = {}
for d in data:
	keyword[d['\xef\xbb\xbfkeyword']] = int(d['importance'])

dataC = []
with open("SentenceExpression_List.csv","rb") as f:
	reader = csv.DictReader(f)
	for row in reader:
		dataC.append(row)
		print row

keysentence = {}
for d in dataC:
	keyword[d['\xef\xbb\xbfkeyword'].replace("~","")] = int(d['importance'])

point = 0#
text = "のし袋の使用量は３年間に１５％減少している。"
node = m.parseToNode(text)
ans = ""
while node:
	ans += "%s %s\n"%(node.surface,node.feature)
	if node.surface in keyword.keys():
		point += keyword[node.surface]
		print"%s %d"%(node.surface.decode("utf-8"),keyword[node.surface])
	node = node.next
print point
		
f = open("node.txt","w")
f.write(ans)
f.close()

#key = ['\xef\xbb\xbfkeyword', 'type', 'importance', 'list1', 'list3', 'list2']
#print(key)

#with open("Output.csv","wb") as f:
#	writer = csv.DictWriter(f,key)
#	key_row = {}
#	for k in key:
#		key_row[k] = k
#	writer.writerow(key_row)
#	for row in data:
#		writer.writerow(row)