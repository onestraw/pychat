# -*- coding: utf-8 -*-

import os
import time


def curTime():
    return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


def check_dir(d):
    """create directory if not exist"""
    if not os.path.exists(d):
        os.makedirs(d)


def check_file(f):
    """create file if not exist"""
    if not os.path.exists(f):
        open(f, 'a').close()
