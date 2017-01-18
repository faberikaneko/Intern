# -*- encode:utf-8-sig -*-

"""sandbox test area
	now: sql request"""

import sqlite3

import csv

import codecs

def hogehoge():
	None

if __name__ == "__main__":
	dbname = "test.db".encode("utf-8")
	connection = sqlite3.connect(dbname)
	connection.text_factory = unicode
	cursor = connection.cursor()

	answer = cursor.execute(u"""SELECT count(*) FROM sqlite_master WHERE type=? AND name=?""",(u"table",u"listOne")).next()
	if answer[0] != 0:
		cursor.execute(u"""DROP TABLE listOne""")

	cursor.execute(u"""CREATE TABLE listOne\n(name ntext, weight real)""")
	addMessage = u"""INSERT INTO listOne VALUES (?,?)"""
	with open("ClueWord_List.csv","r") as file:
		reader = csv.reader(file)
		header = next(reader)
		for word in reader:
			cursor.execute(addMessage,(word[0].decode("utf-8"),int(word[2].decode("utf-8"))))
	connection.commit()
	cursor.execute(u"""SELECT * FROM listOne""")
	answers = cursor.fetchall()
	with codecs.open("test.csv","w",encoding="utf-8-sig") as file:
		for answer in answers:
			uni = answer[0].encode("utf-8")
			file.write(answer[0])
			file.write(",")
			file.write(str(answer[1]))
			file.write("\n")