#!/usr/bin/env python3

import os
import subprocess
import multrunchk

if multrunchk.chekMultipleRun('nph-start.py', 'drive_recorder') == True:
    rst = subprocess.Popen(['sudo', 'systemctl', 'start', 'drive_recorder.service'])


# HTTPレスポンスヘッダ 
print('HTTP/1.1 302 Found')
print('Location: ../index.html')
print('')


