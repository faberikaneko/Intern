# 難易度推定
import MeCab
import sys

m = MeCab.Tagger("-Owakati")
 
fin = open('./target.txt','r')

fcorpus = []
for i in range(1,13):
    print i
    fcorpus.append(open('./corpus/kanji_level'+str(i)+'.csv',"r"))

fout = open('./result.txt','w')

# 対象テキストを文字ベースに分割
word = []
for line in fin.read().decode('utf-8'):
    for i in line:
        word.append(i.encode('utf-8'))
        fout.write(i.encode('utf-8')+" ")
print "END"