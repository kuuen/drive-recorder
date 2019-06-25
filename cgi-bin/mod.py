#!/usr/bin/env python3

import os
import subprocess
import argparse
import cgi


# 起動引数
form = cgi.FieldStorage()
mvNo = form.getvalue('mv-no','')
text = ''
path = '/home/pi/work/DriveRecoder/html/drive/'

# 引数が不正なら処理しない。 ファイル名は数値.mp4の形式
if (mvNo.isdecimal() == False) :
  text = 'param error no numeric :' + mvNo
else:
  # 対象のファイルがあるか調べる。なければ処理しない
  if (os.path.exists(path + "{0}.mp4".format(int(mvNo))) == False):
    text = 'param erro nothing number:' + mvNo
  else:

    # パフォーマンスの向上のため録画を停止する。
    rst = subprocess.Popen(['sudo', 'systemctl', 'stop', 'drive_recorder.service'])


    cmd = "ffmpeg -i " + path + "{0}.mp4 -vcodec copy -acodec -c ".format(int(mvNo)) + path + "{0}new.mp4 -loglevel quiet".format(int(mvNo))

    subprocess.call(cmd.split())
    # オリジナルの削除は最後に
    os.rename(path + "{0}.mp4".format(int(mvNo)), path + "{0}old.mp4".format(int(mvNo)))
    os.rename(path + "{0}new.mp4".format(int(mvNo)), path + "{0}.mp4".format(int(mvNo)))
    os.remove(path + "{0}old.mp4".format(int(mvNo)))

    # 録画の再開。もともと録画していない場合だとこれはおかしいが気にしない
    rst = subprocess.Popen(['sudo', 'systemctl', 'start', 'drive_recorder.service'])
    text = "ok "

# クライアントへ返す文字列を作成。index.htmlへリダイレクトさせる
result = '''Content-Type: text/html

<html>
<head><meta charset='utf-8'/>
<style type='text/css'>
body {{font-size: 1.4em;}}
</style>
</head>
<body>
{}
<button id="btn-move-index" class="btn buttonex" onclick="location.href='../index.html'">GoToIndex</button>
</body>
</html>
'''

# クライアントへレスポンス
print(result.format(text))

