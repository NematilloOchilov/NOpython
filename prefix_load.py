#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

with open('jsondb/prefix.json') as f:
    data = json.load(f)
for i in data:
    print(data[i])
