#!/usr/bin/env python3

import os
import subprocess
import multrunchk
import time

url = ''
if 'HTTP_HOST' in os.environ:
    url = os.environ['HTTP_HOST']
else:
    url = 'no Key HTTP_HOST'

#url = 'http://' + url + ':8081/'
url = '../../motion.html'


if multrunchk.chekMultipleRun('nph-start-motion.py', 'sudo motion -b') == False:
    # HTTPレスポンスヘッダ
    print('HTTP/1.1 302 Found')
    print('Location: ' + url)
    print('')
    quit()

rst = subprocess.Popen(['sudo', 'systemctl', 'stop', 'drive_recorder.service'])


cmd = 'ps aux | grep motion'
proc = subprocess.Popen(cmd, shell  = True, stdin  = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
flgRunning = False
for s in  proc.stdout:
    if s.find(b'motion -b')  != -1 :
        flgRunning = True

if flgRunning == False :
    rst = subprocess.Popen(['sudo', 'motion', '-b'])

time.sleep(3)

# HTTPレスポンスヘッダ
print('HTTP/1.1 302 Found')
print('Location: ' + url)
print('')

