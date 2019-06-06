#!/usr/bin/env python3

import os
import subprocess

dataDir = '/media/data/driveRecoder/'
# Make new file name
all_files = os.listdir(dataDir)
current_numbers = []
for file_name in all_files:
#    current_numbers.append(int(file_name[:-4]))
    s = file_name[:-4]

    if (s.isdecimal()):
        current_numbers.append(int(s))

current_numbers.sort()
if (current_numbers):
    next_number = current_numbers[-1] + 1
else:
    next_number = 0
new_filename = "{}".format(next_number)

# Check disk space
if (current_numbers):
    remove_number = current_numbers[0]
    p = subprocess.Popen("df -h".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

#    disk_space = int(p.stdout.readlines()[1].split()[4][:-1])

    disk_space = 0
    for pr in p.stdout:
        if pr.split()[0] == b'/dev/mmcblk0p8':
            #print(pr)
            disk_space = int(pr.split()[4][:-1])
            break

    if (70 < disk_space):
        subprocess.call("rm {}{}.mp4".format(dataDir, remove_number).split())

fname = "{}{}.mp4"

cmd = "ffmpeg -f v4l2 -input_format mjpeg -framerate 30 "
cmd += "-video_size 720x480 "
#cmd += "-video_size 1440x1080 "

cmd += "-i /dev/video0 -c:v h264_omx  -metadata:s:v:0 rotate=0 -b:v 6500k -c:a aac -b:a 32k -f matroska "

cmd += "-vf drawtext=\"fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf:fontcolor=#FFFFFF:fontsize=30:text='%{localtime}'\" "
cmd += "-t 00:15:00 -loglevel quiet "
cmd += fname.format(dataDir, new_filename)

print('test')
subprocess.call(cmd.split())
