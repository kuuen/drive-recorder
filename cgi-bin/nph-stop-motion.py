#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
import multrunchk
import urllib.request
import time

# motionのipアドレス取得
url = ''
if 'HTTP_HOST' in os.environ:
  url = 'http://' + os.environ['HTTP_HOST'] + ':8080/0/action/quit'

# motionを止httpのアクセスで止めに行く。他にいいやり方はあるか？
# motion -b で起動、バッググラウンドで作動でサービスでない。killもあるがPID探すのが面倒
if url != '' :
  req = urllib.request.Request(url)

  # 不要だがレスポンスは受け取っておく
  with urllib.request.urlopen(req) as res:
    body = res.read()

time.sleep(3)

print('HTTP/1.1 302 Found')
print('Location: ../index.html')
print('')

