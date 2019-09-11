#!/usr/bin/env python3


# 動画ファイル完成通知
# motionのon_movie_end イベントは直ぐに終了させないと強制的に終了する模様。
# ここでgoogle Driveにアップロードするには時間が掛かり過ぎるからtcpで他のプロセスにアップロードを依頼する
# Loggerの設定完了する前にプロセスが中断されることもあったから処理は必要最低限にする

import argparse
import socket
from logging import getLogger, StreamHandler, FileHandler ,DEBUG, INFO, ERROR, Formatter
from logging.handlers import TimedRotatingFileHandler

logger = getLogger(__name__)

def logsetting():
  # ログファイルに設定
  logFileName = '/var/log/kanshi_camera/notification_log.txt'

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


# logsetting()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--terget', help='対象ファイルをフルパスで指定' ,required=True)
args = parser.parse_args()

logger.debug('引数:' + args.terget)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  # サーバを指定
  s.connect(('127.0.0.1', 3321))
  # サーバにメッセージを送る
#  s.sendall(b'args.terget')
  s.sendall(args.terget.encode('utf-8'))

  # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
  data = s.recv(1024)
  #
  print(repr(data))

