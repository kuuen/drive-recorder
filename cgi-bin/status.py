#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os

cmd = 'ps aux'

proc = subprocess.Popen(cmd, shell  = True, stdin  = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
flgRunningMotion = 0
flgRunningRecorder = 0
msg = ''
for s in  proc.stdout:
    if s.find(b'motion -b')  != -1 :
        flgRunningMotion = 1
    elif s.find(b'drive_recorder.sh') != -1:
        flgRunningRecorder = 1

if flgRunningMotion == 1:
    msg += 'motion on \n'
else:
    msg += 'motion off \n'

if flgRunningRecorder == 1:
    msg += 'recorder on \n'
else:
    msg += 'rcorder off \n'

url = ''
if 'HTTP_HOST' in os.environ:
    url = os.environ['HTTP_HOST']
else:
    url = 'no Key HTTP_HOST'

motionStopLink = 'http://' + url + ':8080/0/action/quit'

print("Content-type: application/json")
print("\n\n")

#data = sys.stdin.read()
#params = json.loads(data)
text = 'abara'

text = msg
result = {'text': text, 
    'r_motion': flgRunningMotion, 
    'r_recorder': flgRunningRecorder, 
    'motion_stop_link' : motionStopLink,
    'msg': msg  }

print(json.JSONEncoder().encode(result))
print('\n')


