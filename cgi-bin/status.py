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

# ps コマンドの結果を1行づつ確認
for s in  proc.stdout:
    # motionとサービスのプロセスが動いているか確認 sをutf8に変換したほうがコード見やすかったか？
    if s.find(b'motion -b')  != -1 :
        flgRunningMotion = 1
    elif s.find(b'drive_recorder.sh') != -1:
        flgRunningRecorder = 1

# クライアントに返す値を作成
if flgRunningMotion == 1:
    msg += 'motion on \n'
else:
    msg += 'motion off \n'

if flgRunningRecorder == 1:
    msg += 'recorder on \n'
else:
    msg += 'rcorder off \n'

# motion停止指示urlを作成
url = ''
if 'HTTP_HOST' in os.environ:
    url = os.environ['HTTP_HOST']
else:
    url = 'no Key HTTP_HOST'

motionStopLink = 'http://' + url + ':8080/0/action/quit'

# レスポンス お約束の文字列で改行なんかもそれに従わないとブラウザによっては正しく動かない
print("Content-type: application/json")
print("\n\n")

#data = sys.stdin.read()
#params = json.loads(data)

text = msg
result = {'text': text, 
    'r_motion': flgRunningMotion, 
    'r_recorder': flgRunningRecorder, 
    'motion_stop_link' : motionStopLink,
    'msg': msg  }

# json形式で返す
print(json.JSONEncoder().encode(result))
print('\n')
