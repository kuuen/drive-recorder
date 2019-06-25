#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os

cmd = 'ps aux'
# この挙動に意味がない。削除するか？
proc = subprocess.Popen(cmd, shell  = True, stdin  = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

# motionのページurlを作成。
url = ''
# 環境変数からipアドレスを取得
# 取得できない場合はmotionのストリーミングを表示できないがどうするか？
if 'HTTP_HOST' in os.environ:
    url = os.environ['HTTP_HOST']
else:
    url = 'no Key HTTP_HOST'

screenurl = 'http://' + url + ':8081/index.html'

print("Content-type: application/json")
print("\n\n")

#data = sys.stdin.read()
#params = json.loads(data)
# 無意味な文字列
text = 'abara'

result = {'text': text,
    'motionurl' : 'http://' + url,
    'screenurl': screenurl  }

# レスポンス
print(json.JSONEncoder().encode(result))
print('\n')


