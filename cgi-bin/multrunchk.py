#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess


def chekMultipleRun(cmd, service):
    """
    多重コマンド発行防止。指定したコマンドが起動中の場合、サービスが既に稼働中の場合False
    を返す
    """

    if service == '':
        service = 'non check'

    cmdps = 'ps aux'
    proc = subprocess.Popen(cmdps, shell  = True, stdin  = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    i = 0
    svchk = True
    for s in  proc.stdout:
        str = s.decode('utf-8')

        if str.find(cmd)  != -1 :
            i += 1

        if str.find(service) != -1 :
            svchk = False
            break

    if i >= 2 or svchk == False:
        return False
    else:
        return True
