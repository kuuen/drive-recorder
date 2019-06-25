#!/usr/bin/env python3

import os
import subprocess
import multrunchk

# 多重起動チェックの後に録画を止める
if multrunchk.chekMultipleRun('nph-stop.py', '') == True:
    rst = subprocess.Popen(['sudo', 'systemctl', 'stop', 'drive_recorder.service'])

print('HTTP/1.1 302 Found')
print('Location: ../index.html')
print('')


