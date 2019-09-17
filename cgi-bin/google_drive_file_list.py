#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os
import glob
import time
import json
from operator import itemgetter

# パスは環境変数にいつか入れたい
dataDir = '/media/data/driveRecoder/'


result_list = {}
with open(dataDir + "google_file_list.json", 'r') as f:
  json_data = json.load(f)

#  print(json_data)
  # 作成日付の降順で並び替え
  result_list = sorted(json_data['list'], key=lambda x:x['createdDate'], reverse = True)


'''
# importに10秒がかかる
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive


# OAuth
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

# 保存先フォルダを指定する　何故かブラウザから作成したフォルダが取得できない
# google drive api で作成したフォルダには保存ができる
folder_id = drive.ListFile({'q': 'title = "kanshi"'}).GetList()[0]['id']

# gooeleDriveにあるファイルリストを取得。サブフォルダは見ない
file_list = drive.ListFile({'q': '"{}" in parents and trashed = false'.format(folder_id)}).GetList()

# 作成日付の降順で並び替え
dsp_list = sorted(file_list, key=lambda x:x['createdDate'], reverse = True)

result_list = []
for f in dsp_list:
#  print(f['title'], ' \t', f['id'], ' \t', f['createdDate'], ' \t', f['fileSize'], ' \t', f['alternateLink'])
  ary = {}
  ary['name'] = f['title']
  ary['link'] = f['alternateLink']
  result_list.append(ary)
'''

print("Content-type: application/json")
print("\n\n")


# 無意味な文字列
text = 'abara'

result = {'text': text,
    'motionurl' : 'ttest',
    'list': result_list  }

# レスポンス
print(json.JSONEncoder().encode(result))
print('\n')


