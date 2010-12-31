#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import random
import uuid

class Omikuji:
	def getWords(self,input):
		d = datetime.datetime.today()
		random.seed(str(uuid.getnode()) + d.strftime("%Y%m%d"))
		if(input == "おみくじ"):
			un = ["大凶","凶","末吉","吉","小吉","中吉","大吉"]
			return [un[random.randint(0,len(un)-1)]]
		elif(input=="おとしだま"):
			return [str(random.randint(0,1000000)) + "円"]
		else:
			return []

if __name__ == "__main__":
	print "Testing:"
	print Omikuji().getWords("おみくじ")
