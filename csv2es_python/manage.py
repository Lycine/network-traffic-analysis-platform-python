# -*- coding: utf-8 -*-
import sys
import json
config_path = []
# config_path = '/home/hongyu/PycharmProjects/bistu-internet-analysis/csv2es_python/config.json'
try:
    for argv in sys.argv:
        config_path.append(argv)
        print 'config_path: ' + config_path
except:
    print 'no decalre config_path'
if len(config_path) == 0:
    config_path.append()
with open(config_path, 'r') as f:
    val = f.read()
    config = json.loads(val)

FINISHED_DIR = config['dir']['FINISHED_DIR']
PENDING_DIR = config['dir']['PENDING_DIR']