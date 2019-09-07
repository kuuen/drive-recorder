#!/usr/bin/env python3


# クライアントを作成
import argparse
import socket
from logging import getLogger, StreamHandler, FileHandler ,DEBUG, INFO, ERROR, Formatter
from logging.handlers import TimedRotatingFileHandler


# ログファイルに設定
logFileName = '/var/log/drive_recoder/uploadclientlog.txt'

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

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--terget', help='対象ファイルをフルパスで指定' ,required=True)
args = parser.parse_args()

logger.debug('引数:')
logger.debug(args.terget)

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

