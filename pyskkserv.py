#!/usr/bin/python
# -*- coding:utf-8 -*-

#Listenするホストとポート
HOST = 'localhost'
PORT = 1178

#モジュールをインポート
from mod.CurrentTime import CurrentTime
from mod.GoogleAPI import GoogleIME
from mod.Twitter import Twitter
from mod.Omikuji import Omikuji

import sys
from libpyskkserv import *

if __name__ == "__main__":
	if len(sys.argv)>1:
		PORT = int(sys.argv[1])
	PySKKServ().start(HOST,PORT,
			[#("いま|きょう|now|today",CurrentTime),
			 #(".+",GoogleIME),
			 ("ぬ.+",Twitter),
			 ("おみくじ|おとしだま",Omikuji)
			]
			,debug_out = True)
