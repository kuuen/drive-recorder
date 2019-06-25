#!/usr/bin/env python3

import os
import subprocess
import multrunchk
import time
import glob
from operator import itemgetter


def oldmotionDel():
  """
  古いmoton動画ファイルを削除
  4つ前のファイルは削除する
  """
  # 環境変数なりにしたほうがいいか？同フォルダにmp4もあるがそれは対象外
  # 残り容量を考えてのことだから全動画ファイルを考慮しての設計にしないといけない気がする
  dataDir = '/media/data/driveRecoder/*.avi'
  
  # ファイル一覧取得
  files = glob.glob(dataDir)

  if len(files) < 5:
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
  # 古いファイルを削除していく
  # 4つ以降古いやつは削除する
  for file in lst:
    if i < 0 :
      break;
    os.remove(file[0])
    i -= 1 

# motionのurl取得　同じことを他でもやってるから共通化したほうがいいか？そもそもこの値は使用していない。いつか削除する
url = ''
if 'HTTP_HOST' in os.environ:
  url = os.environ['HTTP_HOST']
else:
  url = 'no Key HTTP_HOST'

#url = 'http://' + url + ':8081/'
url = '../../motion.html'

# 多重起動チェックmotionが既に動いていたら何もしない
if multrunchk.chekMultipleRun('nph-start-motion.py', 'sudo motion -b') == False:
  # HTTPレスポンスヘッダ
  print('HTTP/1.1 302 Found')
  print('Location: ' + url)
  print('')
  quit()

# 録画停止。motionと録画は同時に実行しない。多分できない。できてもパフォーマンスはひどく悪くなる
rst = subprocess.Popen(['sudo', 'systemctl', 'stop', 'drive_recorder.service'])
# 古いmotion動画を削除
oldmotionDel()

# motion多重起動チェック。上のやつは自身のスクリプト、これはmotionのプロセス
cmd = 'ps aux | grep motion'
proc = subprocess.Popen(cmd, shell  = True, stdin  = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
flgRunning = False
# 既にmotonが動いていれば、開始コマンドは発行しないようにする
for s in  proc.stdout:
  if s.find(b'motion -b')  != -1 :
    flgRunning = True

# 多重起動していないか確認した後にmotion起動。たしかmotionは同時実行できたはずだから注意する
if flgRunning == False :
  rst = subprocess.Popen(['sudo', 'motion', '-b'])

# レスポンスを返す前に少し待つ。クライアントにリダイレクト後にmotionのurlにアクセス
# しにくるがmotionがストリーム開始していないとクライアントでは404とかになってエラー表示になる
time.sleep(3)

# HTTPレスポンスヘッダ
print('HTTP/1.1 302 Found')
print('Location: ' + url)
print('')

