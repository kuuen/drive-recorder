#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess


def chekMultipleRun(cmd, service):
    """
    多重コマンド発行防止。指定したコマンドが起動中の場合、サービスが既に稼働中の場合False
    を返す
    cmd=コマンドの文字列を指定
    service=サービスの場合はサービス名を指定する
    """

    if service == '':
        service = 'non check'

    cmdps = 'ps aux'
    proc = subprocess.Popen(cmdps, shell  = True, stdin  = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    i = 0
    svchk = True
    # psコマンドの結果を１行づつ取得してチェックする
    for s in  proc.stdout:
        # utf8として文字列を読まないとうまくいかなかった為だったはず
        str = s.decode('utf-8')

        # 対象のコマンドか？
        # psコマンド自体も結果に上がるので最後まで確認する
        if str.find(cmd)  != -1 :
            i += 1

        # 対象のサービスか？ヒットしたら既に稼働中なのでループを抜ける
        if str.find(service) != -1 :
            svchk = False
            break

    # 2以上の条件はpsコマンドの結果は省くため
    if i >= 2 or svchk == False:
        return False
    else:
        return True
