# -*- coding: utf-8 -*-

import os

# config
IP = "127.0.0.1"
PORT = 6677
DGRAM_FORMAT = "50s50s50s200s"
BASE_DIR = './demo'
DEBUG = True
PID_FILE = os.path.join(BASE_DIR, 'pychat_server.pid')
LOG_FILE = os.path.join(BASE_DIR, 'pychat_server.log')

# const
USER_PATH = os.path.join(BASE_DIR, 'user')
MSG_PATH = os.path.join(BASE_DIR, 'msg')
FILE_PATH = os.path.join(BASE_DIR, 'file')


history_msg_file = os.path.join(MSG_PATH, 'history.pk')
offline_msg_file = os.path.join(MSG_PATH, 'offline.pk')


user_file = os.path.join(USER_PATH, 'user.pk')
friend_file = os.path.join(USER_PATH, 'friends.pk')


file_info = os.path.join(FILE_PATH, 'file_info.txt')


def check_dir(d):
    """create directory if not exist"""
    if not os.path.exists(d):
        os.makedirs(d)


def check_file(f):
    if not os.path.exists(f):
        open(f, 'a').close()


check_dir(USER_PATH)
check_dir(MSG_PATH)
check_dir(FILE_PATH)
check_file(file_info)
