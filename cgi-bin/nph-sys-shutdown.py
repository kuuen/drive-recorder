#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
import multrunchk
import time

# 多重起動チェック
if multrunchk.chekMultipleRun('nph-sys-shutdown.py', '') == False:
  print('HTTP/1.1 302 Found')
  print('Location: ../index.html')
  print('')
  quit()

# nph-sys-reboot.pyと同様visudoに登録が必要
subprocess.Popen(['sudo', '/sbin/shutdown', '-h', 'now'])

print('HTTP/1.1 302 Found')
print('Location: ../index.html')
print('')
