# encoding:utf-8

"""sandbox test area
	now: regular expression"""

import regex as re

import codecs

if __name__ == "__main__":
	print re.findall(u"hoge",u"fuga") != None
	sep = ur"(?P<all>(?:[^]{「《【『［〈≪（＜｛{()}｝＞）≫〉］』】》」。]*(?P<rec>[[「《【『［〈≪（＜｛[{(](?:[^]{「《【『［〈≪（＜｛{()}｝＞）≫〉］』】》」]*|(?P&rec))*[])}｝＞）≫〉］』】》」]))+.*?。)"
	pattern = ur"(?:[^「。]*「[^」]*」)*.*?。"
	with codecs.open("input_sunaba.txt",mode="r",encoding="utf-8-sig") as file:
		texts = re.sub(ur"\n|\r","","".join(file.readlines()))
	#rematch = re.compile(pattern)
	#anslist = rematch.findall(texts)
	anslist = map(lambda x:x.group(),re.finditer(sep,texts))
	with codecs.open("output_sunaba.txt",mode="w",encoding="utf-8-sig") as file:
		file.write(u"\r\n".join(map(lambda x:x if isinstance(x,unicode) else u",".join(x),anslist)))