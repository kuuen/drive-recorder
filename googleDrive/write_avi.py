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


# 保存先フォルダを指定する　何故かブラウザから作成したフォルダが取得できない
# google drive api で作成したフォルダには保存ができる
folder_id = drive.ListFile({'q': 'title = "kanshi"'}).GetList()[0]['id']
f = drive.CreateFile({"parents": [{"id": folder_id}]})
f.SetContentFile('01-20190828112023.avi')
f['title'] = 'test.avi'


print("upload start: " + datetime.datetime.now().strftime("%H:%M:%S"))
f.Upload()
print("upload end: " + datetime.datetime.now().strftime("%H:%M:%S"))

print(type(f['parents']))
pprint.pprint(f['parents'])
