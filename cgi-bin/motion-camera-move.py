#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os
import multrunchk
import RPi.GPIO as GPIO
import time

PIN_TOP_IN1 = 22
PIN_TOP_IN2 = 23
PIN_LEFT_IN1 = 17
PIN_LEFT_IN2 = 27


def move(pin1, pin2, pin1i, pin2i, moveTime = 0.2) :
  """
  GPIO操作
  pin1,pin2 はGPIOの番号を指定、第二、三引数は GPIO.OUT,GPIO.LOWを指定
  moveTimeは作動時間デフォルト0.2秒
  """
  GPIO.setmode(GPIO.BCM)

  # 第二引数 GPIO.OUT か GPIO.LOW
'''
  GPIO.setup(pin1, GPIO.OUT)
  GPIO.setup(pin2, GPIO.OUT)
  time.sleep(moveTime)
  GPIO.output(pin1,GPIO.LOW)
  GPIO.output(pin1,GPIO.LOW)

  GPIO.cleanup()
'''

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
if multrunchk.chekMultipleRun('nph-camera-move.py', '') == False:
  responce('ng:作動中')

# 値存在チェックは本来は必要である。そのまま起動するとここで待ちとなる
data = sys.stdin.read()
params = json.loads(data)
move = int(params['move'])

# 値チェック
if move > 1 and move > 4:
  responce('ng:param error')


responce('ok')



