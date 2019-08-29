#!/usr/bin/env python3

import datetime
import pprint
print("import start: " + datetime.datetime.now().strftime("%H:%M:%S"))

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

print("import end: " + datetime.datetime.now().strftime("%H:%M:%S"))

# OAuth

print("Auth start: " + datetime.datetime.now().strftime("%H:%M:%S"))
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)
print("Auth start: " + datetime.datetime.now().strftime("%H:%M:%S"))

# フォルダ指定
folder_id = drive.ListFile({'q': "title = 'kanshi'"}).GetList()[0]['id']
# フォルダ内の内容を取得。サブフォルダは見ない
file_list = drive.ListFile({'q': '"{}" in parents and trashed = false'.format(folder_id)}).GetList()

# 作成日付の昇順で並び替え
dsp_list = sorted(file_list, key=lambda x:x['createdDate'])

for f in dsp_list:
  print(f['title'], ' \t', f['id'], ' \t', f['createdDate'], ' \t', f['fileSize'])
