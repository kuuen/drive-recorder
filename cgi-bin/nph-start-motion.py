#!/usr/bin/env python3

import os
import subprocess
import multrunchk
import time
import glob
from operator import itemgetter


def oldmotionDel():
  dataDir = '/media/data/driveRecoder/*.avi'
  files = glob.glob(dataDir)

  if len(files) <= 5:
    return

  # ファイル名、サイズ、日付からなるリストを作る
  file_lst = []
  for file in files:
    file = os.path.join(dataDir, file)
    #print file,os.stat(file).st_size,time.ctime(os.stat(file).st_mtime)
    file_lst.append([file,os.stat(file).st_size,time.ctime(os.stat(file).st_mtime)])

  # 日付を古い順に並び替える
  lst = sorted(file_lst,key=itemgetter(2), reverse = False)

  i = len(files) - 5
  for file in lst:
    if i < 1 :
      break;
    os.remove(file[0])
    i -= 1 

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

oldmotionDel()

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

