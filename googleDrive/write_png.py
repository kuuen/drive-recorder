#!/usr/bin/env python3

import pprint
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# OAuth
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

# フォルダmoviにファイルをアップロード

# 保存先フォルダを指定する　何故かブラウザから作成したフォルダが取得できない
# google drive api で作成したフォルダには保存ができる
folder_id = drive.ListFile({'q': 'title = "kanshi"'}).GetList()[0]['id']
f = drive.CreateFile({"parents": [{"id": folder_id}]})
f.SetContentFile('test.png')
f['title'] = 'himarin2.png'

# write text to google drive
#f = drive.CreateFile({'title': 'test.png', 'mimeType':'image/png'})
#f.SetContentFile('test.png')
f.Upload()

print(type(f['parents']))
pprint.pprint(f['parents'])
