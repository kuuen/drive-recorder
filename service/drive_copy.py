#!/usr/bin/env python3

import os
import subprocess
import argparse

path = "/home/pi/work/DriveRecoder/data/"

# 起動引数
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileno', help='対象のファイル番号 -m now' ,required=True)
args = parser.parse_args()

no = args.fileno

cmd = "ffmpeg -i /home/pi/work/DriveRecoder/data/{0}.mp4 -vcodec copy -acodec -c /home/pi/work/DriveRecoder/data/{1}new.mp4".format(int(no), int(no))

subprocess.call(cmd.split())

os.rename("/home/pi/work/DriveRecoder/data/{0}.mp4".format(int(no)), "/home/pi/work/DriveRecoder/data/{0}old.mp4".format(int(no)))
os.rename("/home/pi/work/DriveRecoder/data/{0}new.mp4".format(int(no)), "/home/pi/work/DriveRecoder/data/{0}.mp4".format(int(no)))
os.remove("/home/pi/work/DriveRecoder/data/{0}old.mp4".format(int(no)))



