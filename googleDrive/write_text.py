#!/usr/bin/env python3

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# OAuth
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

# write text to google drive
f = drive.CreateFile({'title': 'test.txt'})
f.SetContentString('腰が痛いし、暑い')
f.Upload()
