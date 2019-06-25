#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
import multrunchk
import time


# 多重起動チェック
if multrunchk.chekMultipleRun('nph-sys-reboot.py', '') == False:
  print('HTTP/1.1 302 Found')
  print('Location: ../index.html')
  print('')
  quit()

# 再起動コマンド発行。事前にvisudoに登録しておく必要がある
subprocess.Popen(['sudo', '/sbin/reboot'])

# 処理結果を返すほうが親切か？
print('HTTP/1.1 302 Found')
print('Location: ../index.html')
print('')

