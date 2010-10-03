#!/usr/bin/python
# -*- coding:utf-8 -*-

#Listenするホストとポート
HOST = 'localhost'
PORT = 1178

#モジュールをインポート
from mod.CurrentTime import CurrentTime


import sys
from libpyskkserv import *

if __name__ == "__main__":
	if len(sys.argv)>1:
		PORT = int(sys.argv[1])
	PySKKServ().start(HOST,PORT,
			[("いま|きょう|now|today",CurrentTime)]
			,debug_out = True)
