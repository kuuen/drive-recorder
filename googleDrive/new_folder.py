#!/usr/bin/env python3

import pprint

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

f_folder = drive.CreateFile({'title': 'kanshi',
                             'mimeType': 'application/vnd.google-apps.folder'})
print(f_folder)

f_folder.Upload()

pprint.pprint(f_folder)

