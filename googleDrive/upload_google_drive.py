#!/usr/bin/env python3

#import argparse
import os
import datetime
import pprint
import socket
import glob
import time
from operator import itemgetter

from logging import getLogger, StreamHandler, FileHandler ,DEBUG, INFO, ERROR, Formatter
from logging.handlers import TimedRotatingFileHandler

# ログファイルに設定
logFileName = '/var/log/drive_recoder/uploadlog.txt'

# ログの出力レベル
logLevel = DEBUG

# ログ出力の設定------↓
logger = getLogger(__name__)
handler_format = Formatter('%(asctime)s - %(levelname)s - %(message)s')

# StreamHandlerはprint()と同じ働きではない。実行環境によってsyslogや
# コンソールに出力されることはあっても現状ではhttpのレスポンスに流せるない
handler = StreamHandler()
handler.setLevel(logLevel)
handler.setFormatter(handler_format)

trfh = TimedRotatingFileHandler(
    filename = logFileName,
    backupCount = 6,
    when='midnight',
    encoding='utf-8')

trfh.setLevel(logLevel)
trfh.setFormatter(handler_format)

logger.setLevel(logLevel)
logger.addHandler(handler)
logger.addHandler(trfh)
logger.propagate = False

# カレントディレクトリの変更
os.chdir(os.environ['GOOLE_UPLOAD_HOME']) 


def uploadFile(fileName):

  # OAuth

  logger.debug("Auth start: " + datetime.datetime.now().strftime("%H:%M:%S"))
  gauth = GoogleAuth()
  gauth.CommandLineAuth()
  drive = GoogleDrive(gauth)
  logger.debug("Auth end: " + datetime.datetime.now().strftime("%H:%M:%S"))

  # 保存先フォルダを指定する　何故かブラウザから作成したフォルダが取得できない
  # google drive api で作成したフォルダには保存ができる
  folder_id = drive.ListFile({'q': 'title = "kanshi"'}).GetList()[0]['id']

  # gooeleDriveにあるファイルリストを取得。サブフォルダは見ない
  file_list = drive.ListFile({'q': '"{}" in parents and trashed = false'.format(folder_id)}).GetList()

  # 作成日付の昇順で並び替え
  dsp_list = sorted(file_list, key=lambda x:x['createdDate'])

  # 容量を確認
  size = 0
  for f in dsp_list:
    print(f['title'], ' \t', f['id'], ' \t', f['createdDate'], ' \t', f['fileSize'])
    size = size + int(f['fileSize'])

  logger.debug('upload total size= ' + str(size))

  # 動画ファイルフォルダが10GBを超えている場合は、そのサイズになるまでファイルを削除
  for f in dsp_list:
    if size < 10000000000:
      break

    # ファイルを特定
    f = drive.CreateFile({'id': f['id']})
    size = size - int(f['fileSize'])

    logger.debug("google drive Delete: " + f['title'])
    # gooleDriveを削除する。ゴミ箱にも入らない。ゴミ箱に移動はf.Trash() ゴミ箱から戻すにはf.UnTrash()
    f.Delete()

  logger.debug('upload total size(整理後)= ' + str(size))

  # ロード処理
  f = drive.CreateFile({"parents": [{"id": folder_id}]})
  f.SetContentFile(fileName)
  f['title'] = os.path.basename(fileName)

  logger.debug("upload start: " + datetime.datetime.now().strftime("%H:%M:%S"))
  f.Upload()
  logger.debug("upload end: " + datetime.datetime.now().strftime("%H:%M:%S"))

  print(type(f['parents']))
  pprint.pprint(f['parents'])

  # アップしたファイルはローカルから削除する
  os.remove(fileName)

# アップロードしそこねたファイルを上げる
def uploads():
  dataDir = os.environ['MOVE_PATH'] + '*.avi'
  files = glob.glob(dataDir)
  
  logger.debug("local files: " + str(len(files)))

  if len(files) < 1:
    return

  file_lst = []
  for file in files:
    file = os.path.join(dataDir, file)
    #print file,os.stat(file).st_size,time.ctime(os.stat(file).st_mtime)
    file_lst.append([file,os.stat(file).st_size,time.ctime(os.stat(file).st_mtime)])

  # 日付を古い順に並び替える
  lst = sorted(file_lst,key=itemgetter(2), reverse = False)

  i = len(files) - 1
  # 古いファイルを削除していく
  # 4つ以降古いやつは削除する
  for file in lst:
    if i < 1 :
      break;

    uploadFile(file[0])
    logger.debug(file[0])
    i -= 1 


# importに10秒がかかる
logger.debug("import start: " + datetime.datetime.now().strftime("%H:%M:%S"))
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
logger.debug("import end: " + datetime.datetime.now().strftime("%H:%M:%S"))


callMotionFile = ""

# ★ここから

# ファイル指定して起動。仮実装。アップロードしそこなったものをまとめてアップする、motionからの
# 呼び出しから指定ファイルのアップロードの2通りを実現したい
#　→実現方法。
# １．起動時にソケット待受 motionからの応答を待つ。受けたファイル名はリストに保持。リストはstaticで他スレッドからの操作を考慮する
# 2.１とは別のスレッドで動作 動画保存ディレクトリ確認。動画が2以上ある場合は、googleDriveにアップロードする
#   その際googleDriveの容量確認して規定量を超えていたら古いファイルから削除していく




uploads()

logger.debug("tcp listen start " + datetime.datetime.now().strftime("%H:%M:%S"))

# motionからtcp通信で受ける。
targetFile = ""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.settimeout(None)
  s.bind(('127.0.0.1', 3321))
  s.listen(1)

  conn, addr = s.accept()
  with conn:
    while True:
      data = conn.recv(1024)

      if not data:
        break
#      print('data : {}, addr: {}'.format(data, addr))
      targetFile = data.decode('utf-8')
      logger.debug('data : {}, addr: {}'.format(targetFile, addr) + datetime.datetime.now().strftime("%H:%M:%S"))
      conn.sendall(b'Received: ok')

try : 
  uploadFile(targetFile)
except Exception as e:
  logger.error(e, "upload error")



logger.debug("end " + datetime.datetime.now().strftime("%H:%M:%S"))


