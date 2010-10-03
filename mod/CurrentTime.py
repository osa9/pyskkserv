#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime

class CurrentTime:
	def getWords(self,input):
		d = datetime.datetime.today()
		if(input == "きょう" or input == "today"):
			return ["%d年%d月%d日" % (d.year,d.month,d.day),
					"%d月%d日" % (d.month,d.day)]
		elif(input == "いま" or input == "now"):
			return [d.strftime("%H:%M:%S")]
		else:
			return []

if __name__ == "__main__":
	print "Testing:"
	print CurrentTime().getWords("きょう")
	print CurrentTime().getWords("いま")
