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

subprocess.Popen(['sudo', '/sbin/reboot'])

print('HTTP/1.1 302 Found')
print('Location: ../index.html')
print('')

