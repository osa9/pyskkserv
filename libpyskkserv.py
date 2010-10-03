#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading
import string
import re
import sys
import traceback
import signal

#C-cをハンドル
end_flag = True
def mysig(signum,frame): end_flag = False
signal.signal(signal.SIGINT,mysig)

#debug print
def print_d(str,show):
	if show:print str

#個々のコネクションとか
class PySKKConnection(threading.Thread):
	def __init__(self,sock,filter,debug_out=False):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.sock = sock
		self.filter = filter
		self.debug_out = debug_out

	#かなりあれ
	def canEncodeEUC(self,s):
		try:
			s.decode("utf-8").encode("euc-jp")
			return True
		except:
			return False

	def makeTranslation(self,words):
		words = filter(self.canEncodeEUC,words)
		if len(words)==0:
			return "4\n"
		else:
			return "1/%s/\n" %  "/".join(words)


	#cmd1 : translation
	def translation(self,input):
		output = []
		for reg,cls in self.filter:
			if re.match(reg,input):
				output += cls().getWords(input)
		
		return self.makeTranslation(output)

	#cmd2 : version
	def version(self):
		return "pyskkserv 0.1\n"

	#cmd3 : hostname:port (Not Implemented and maybe not used)
	def hostinfo(self):
		return "\n"

	#cmd4 : abbreviation (Not Implemented)
	def abbrev(self,input):
		return "4\n"

	#get input string terminated by " "(single space)
	def getInput(self,rest):
		str = rest
		while str[-1:] != " " and str[-2:] != " \n" and str[-3:] != " \r\n":
			str += self.sock.recv(1024).decode("euc-jp").encode("utf-8")
		print_d("input: " + str.rstrip(),self.debug_out)
		return string.rstrip(str)

	def command(self):
		str = self.sock.recv(1024).decode("euc-jp").encode("utf-8")
		cmd = str[0]
		print_d("command: "+cmd,self.debug_out)
		if cmd == "0":
			return "" , False
		elif cmd == "1":
			return self.translation(self.getInput(str[1:])) , True
		elif cmd == "2":
			return self.version() , True
		elif cmd == "3":
			return self.hostinfo() , True
		elif cmd == "4":
			return self.abbrev(self.getInput(str[1:])) , True
		else:
			return "",False
		
	def run(self):
		print_d("connect",self.debug_out)
		while 1:
			try:
				res,cont = self.command()
				if(not cont):break
				print_d("output: " + res.rstrip(),self.debug_out)
				self.sock.send(res.decode("utf-8").encode("euc-jp"))
			except:
				print "exception: ",sys.exc_info()[0]
				print sys.exc_info()[1]
				traceback.print_tb(sys.exc_info()[2])
				break
		self.sock.close()
		print_d("disconnect",self.debug_out)

#skkserv
class PySKKServ:
	def listen(self,host,port,filter,debug_out=False):
		print_d("start",debug_out)
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.bind((host,port))
		s.listen(3)
		while end_flag:
			try:
				sock,addr = s.accept()
				PySKKConnection(sock,filter,debug_out).start()
			except:
				break;
		s.close()
		print_d("bye",debug_out)

	def start(self,host,port,filter,debug_out=False):
		self.listen(host,port,filter,debug_out)
