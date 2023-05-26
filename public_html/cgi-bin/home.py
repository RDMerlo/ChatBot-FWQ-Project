#! /usr/bin/python3
import cgi
import os
import re
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("Content-type: text/html")
with open('assets/frame/header.html', 'r') as file:
    txt = file.read()
    txt = re.sub(r"\s", "", txt)
    out_txt = re.split(r"[()]", txt)
print(out_txt[1])

