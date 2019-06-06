#!/usr/bin/env python3

import subprocess



cmd = 'ps aux | grep motion'

proc = subprocess.Popen(cmd, shell  = True, stdin  = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


#stdout_data, stderr_data = proc.communicate() #処理実行を待つ(†1)
#print (stdout_data)  #標準出力の確認
#print (stderr_data)  #標準エラーの確認

for s in  proc.stdout:
    if s.find(b'motion -b')  != -1 :
        print('running')



