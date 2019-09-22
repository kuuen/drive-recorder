#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os
import glob
import time
from operator import itemgetter
from datetime import datetime as dt
import datetime


# motionのページurlを作成。
url = ''


# パスは環境変数にいつか入れたい
dataDir = '/media/data/driveRecoder/'
files = glob.glob(dataDir + '*')
#logger.debug("local files: " + str(len(files)))


print("Content-type: application/json")
print("\n\n")

file_lst = []
for file in files:
  file = os.path.join(dataDir + '*', file)
  #print file,os.stat(file).st_size,time.ctime(os.stat(file).st_mtime)
  file_lst.append([file, os.stat(file).st_size, time.ctime(os.stat(file).st_mtime)])

# 日付を古い順に並び替える
lst = sorted(file_lst, key=itemgetter(1), reverse = False)

result_list = []
for file in lst:

  if os.path.splitext(file[0])[1] != '.mp4' :
    continue

  ary = {}

  fileName = os.path.basename(file[0])
  ary['link'] = '../drive/' + fileName
  ary['name'] = str(datetime.datetime.strptime(fileName[3:-4], '%Y%m%d%H%M%S'))
  ary['storage_location'] = 'l'


#  if os.path.splitext(file[0])[1] == '.avi' or os.path.splitext(file[0])[1] == '.mp4' :

#  else:
#    ary['link'] = 'non link'

  result_list.append(ary)

# 予め取得したGoogleDriveに保存しているファイルリストを読み込む
google_drive_list = {}
with open(dataDir + "google_file_list.json", 'r') as f:
  json_data = json.load(f)

#  print(json_data)
  # 作成日付の降順で並び替え
  google_drive_list = sorted(json_data['list'], key=lambda x:x['createdDate'], reverse = True)

#print(google_drive_list)
'''
for item in google_drive_list :
  ary = {}
  ary['name'] = item['name']
  ary['link'] = item['link']

  result_list.append(ary)
'''
result_list.extend(google_drive_list)

#data = sys.stdin.read()
#params = json.loads(data)
# 無意味な文字列
text = 'abara'

result = {'text': text,
    'motionurl' : 'ttest',
    'list': result_list  }

# レスポンス
#print(json.JSONEncoder().encode(result))
print(json.JSONEncoder().encode(result))
print('\n')


