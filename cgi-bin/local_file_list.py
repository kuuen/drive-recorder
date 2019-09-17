#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os
import glob
import time
from operator import itemgetter



# motionのページurlを作成。
url = ''


# パスは環境変数にいつか入れたい
dataDir = '/media/data/driveRecoder/*'
files = glob.glob(dataDir)
#logger.debug("local files: " + str(len(files)))


print("Content-type: application/json")
print("\n\n")

file_lst = []
for file in files:
  file = os.path.join(dataDir, file)
  #print file,os.stat(file).st_size,time.ctime(os.stat(file).st_mtime)
  file_lst.append([file, os.stat(file).st_size, time.ctime(os.stat(file).st_mtime)])

# 日付を古い順に並び替える
lst = sorted(file_lst, key=itemgetter(1), reverse = False)

result_list = []
for file in lst:

  ary = {}

  fileName = os.path.basename(file[0])
  ary['name'] = fileName

#  if os.path.splitext(file[0])[1] == '.avi' or os.path.splitext(file[0])[1] == '.mp4' :
  if os.path.splitext(file[0])[1] == '.mp4' :
    ary['link'] = '../drive/' + fileName
  else:
    ary['link'] = 'non link'

  result_list.append(ary)


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


