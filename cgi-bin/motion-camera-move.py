#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os
import multrunchk
import RPi.GPIO as GPIO
import time

# GPIOの番号Positionの番号ではない
PIN_TOP_IN1 = 17
PIN_TOP_IN2 = 27
PIN_LEFT_IN1 = 22
PIN_LEFT_IN2 = 23


def moveCamera(p1, p2, p1i, p2i, mt = 0.2) :
  """
  GPIO操作
  pin1,pin2 はGPIOの番号を指定、第二、三引数は GPIO.OUT,GPIO.LOWを指定
  moveTimeは作動時間デフォルト0.2秒
  """
  
  # 初期化　GPIOの番号指定で操作する
  GPIO.setmode(GPIO.BCM)
  
  # 各ピン出力で使用
  GPIO.setup(p1, GPIO.OUT)
  GPIO.setup(p2, GPIO.OUT)

  # 第二引数 GPIO.HIGH か GPIO.LOW

  GPIO.output(p1, p1i)
  GPIO.output(p2, p2i)

  time.sleep(mt)

  GPIO.output(p1, GPIO.LOW)
  GPIO.output(p2, GPIO.LOW)

  GPIO.cleanup()


def responce(rst) :
  """
  これ呼ぶと終了。jsonで結果をクライアントに返す
  """

  result = {'result': rst}

  print("Content-type: application/json")
  print("\n\n")
  print(json.JSONEncoder().encode(result))
  print('\n')

  # ここに置くとわかりづらいか？
  quit() 


# 多重起動チェック
if multrunchk.chekMultipleRun('motion-camera-move.py', '') == False:
  responce('ng:作動中')

# 起動引数を取得
# httpでリクエストを受けcgiとして起動する想定。コンソールで起動するとここで入力待ちとなってしまう
# 値存在チェックは本来は必要である。
# 改善は必要
data = sys.stdin.read()
params = json.loads(data)
move = int(params['move'])

# パラメータの初期化
pin1 = 0
pin2 = 0
pin1i = GPIO.LOW
pin2i = GPIO.LOW
moveTime = 0.2

# 起動引数によって処理を分岐。右辺を定数にするべき
# 1=上　2=下 3＝左　4=右だったはず
if move == 1 :
  pin1 = PIN_TOP_IN1
  pin2 = PIN_TOP_IN2
  pin1i = GPIO.LOW
  pin2i = GPIO.HIGH
  moveTime = 0.2
elif move == 2 :
  pin1 = PIN_TOP_IN1
  pin2 = PIN_TOP_IN2
  pin1i = GPIO.HIGH
  pin2i = GPIO.LOW
  moveTime = 0.2
elif move == 3 :
  pin1 = PIN_LEFT_IN1
  pin2 = PIN_LEFT_IN2
  pin1i = GPIO.HIGH
  pin2i = GPIO.LOW
elif move == 4 :
  pin1 = PIN_LEFT_IN1
  pin2 = PIN_LEFT_IN2
  pin1i = GPIO.LOW
  pin2i = GPIO.HIGH
else:
  responce('ng:param error')

# gpio制御、モータを動かしてカメラの向きを変える
moveCamera(pin1, pin2, pin1i, pin2i, moveTime)

responce('ok')



