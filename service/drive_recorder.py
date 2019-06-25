#!/usr/bin/env python3

import os
import subprocess

# 動画保存先
dataDir = '/media/data/driveRecoder/'
# 保存先のファイル一覧を取得 Make new file name
all_files = os.listdir(dataDir)
current_numbers = []

# ファイル一覧分ループ
for file_name in all_files:
#    current_numbers.append(int(file_name[:-4]))
    # ファイル名の数値部分を取り出す 12345.mp4 →　12345
    s = file_name[:-4]

    # 取り出した値が正しいか？ motionのファイルは削除対象外。00-yyyyMMddHHmmss.aviの形式
    if (s.isdecimal()):
        current_numbers.append(int(s))
        
# 数値の若い順に並び替え
current_numbers.sort()

# ファイル名の通しの番号決定　ファイルがない場合は0、それ以外は最大値+1
if (current_numbers):
    next_number = current_numbers[-1] + 1
else:
    next_number = 0

new_filename = "{}".format(next_number)

# 容量確認　Check disk space
if (current_numbers):
    # 削除する場合のファイル名を指定
    remove_number = current_numbers[0]
    p = subprocess.Popen("df -h".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

#    disk_space = int(p.stdout.readlines()[1].split()[4][:-1])

    disk_space = 0
    # dfの結果を1行づつ見る
    for pr in p.stdout:
        # 保存先のディスクは以下、dataDirとコーディングが二度手間ではある気がするが実装はこれで
        if pr.split()[0] == b'/dev/mmcblk0p8':
            #print(pr)
            # こんな感じの結果になるので後ろから5番目の値から使用率を取得
            # /dev/mmcblk0p8    20G  2.6G   18G   13% /media/data
            disk_space = int(pr.split()[4][:-1])
            break

    # 使用率が70%超えていたら一番古いファイルを削除。motion動画ファイルを追加したことで１ファイルのみ削除だけでは
    # 足りなくなったりしないか？30%(780MB)と余裕を持たせてあるから満杯にはならないか？フル録画で230MBとなる
    if (70 < disk_space):
        subprocess.call("rm {}{}.mp4".format(dataDir, remove_number).split())

# ffmpegのコマンド作成
# 解像度、フレームレート、録画時間等ブラウザで変更できる仕組みを作成したら検証しやすくなるはず
fname = "{}{}.mp4"

cmd = "ffmpeg -f v4l2 -input_format mjpeg -framerate 30 "
cmd += "-video_size 720x480 "
#cmd += "-video_size 1440x1080 "

cmd += "-i /dev/video0 -c:v h264_omx  -metadata:s:v:0 rotate=0 -b:v 6500k -c:a aac -b:a 32k -f matroska "

cmd += '-vf drawtext=fontfile="/usr/share/fonts/truetype/freefont/FreeSerif.ttf":fontcolor=#FFFFFF:fontsize=30:x=350:y=450:text=%{localtime} '
cmd += "-t 00:15:00 "
cmd += "-loglevel quiet "
cmd += fname.format(dataDir, new_filename)

#print(cmd)
subprocess.call(cmd.split())

#rst = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

#print(cmd.split())
#for rs in rst.stdout:
#    print(rs)

