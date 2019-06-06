#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os

cmd = 'ps aux'

proc = subprocess.Popen(cmd, shell  = True, stdin  = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


url = ''
if 'HTTP_HOST' in os.environ:
    url = os.environ['HTTP_HOST']
else:
    url = 'no Key HTTP_HOST'

screenurl = 'http://' + url + ':8081/index.html'

print("Content-type: application/json")
print("\n\n")

#data = sys.stdin.read()
#params = json.loads(data)
text = 'abara'

result = {'text': text,
    'motionurl' : 'http://' + url,
    'screenurl': screenurl  }

print(json.JSONEncoder().encode(result))
print('\n')


