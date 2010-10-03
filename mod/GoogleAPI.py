#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import json
import urllib
import string
import re

# Google 日本語入力APIから変換候補を取得してリストで返す
# http://www.google.com/intl/ja/ime/cgiapi.html
class GoogleIME:
    def getWords(self,str):
        if(re.search("[a-zA-Z]",str)):
            return []
        url = "http://www.google.com/transliterate?langpair=ja-Hira|ja&text=" + urllib.quote(str)
        content = urllib.urlopen(url).read()
        content = re.sub(",\r?\n?]","]",content)
        #print string.strip(content)
        s = json.loads(string.strip(content))
        return self.encodeList(self.makeList(s))
    def makeList(self,s):
        if len(s)==0:
            return []
        elif len(s)==1:
            return s[0][1]
        else:
            return [x + y for x in s[0][1] for y in self.makeList(s[1:])]
    def encodeList(self,list):
        return map(lambda s : s.encode("utf-8"),list)
