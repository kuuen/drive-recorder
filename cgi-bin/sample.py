#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json

print("Content-type: application/json")
print("\n\n")

data = sys.stdin.read()
params = json.loads(data)
text = params['text']


result = {'text': text}

print(json.JSONEncoder().encode(result))
print('\n')

