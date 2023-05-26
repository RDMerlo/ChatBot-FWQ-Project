#! /usr/bin/python3
import cgi
import os

print('Content-type:text/html\n\n')
referer = os.environ.get('HTTP_REFERER', '/')
param = "?TEXT_1=Дим&TEXT_2=Султанов";
print('<html>')
print('  <head>')
print('    <meta http-equiv="refresh" content="0;url='+str(referer) + str(param) +'" />')
print('  </head>')
print('</html>')
