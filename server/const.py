# -*- coding: utf-8 -*-

import os
from utils import check_dir, check_file


# config
IP = '127.0.0.1'
PORT = 6677
DGRAM_FORMAT = '50s50s50s200s'
CMD_FORMAT = '50s50s50s'
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


check_dir(USER_PATH)
check_dir(MSG_PATH)
check_dir(FILE_PATH)
check_file(file_info)
