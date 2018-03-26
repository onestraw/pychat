# -*- coding: utf-8 -*-

import random
import string
import cPickle
from const import user_file
from logger import logger


# 注册新用户，生成一个6位数的数字串
def register(email, nickname, pwd):
    def new_user():
        return random.randint(100000, 1000000)
    try:
        fr = open(user_file, "rb")
        users = cPickle.load(fr)
        user_no = new_user()
        while user_no in users.keys():
            user_no = new_user()
        fr.close()
    except IOError or EOFError as e:
        logger.error(e)
        users = {}
        user_no = new_user()
    # 添加用户
    fw = open(user_file, "wb")
    fw.truncate()
    users[user_no] = [email, nickname, pwd]
    cPickle.dump(users, fw)  # 重新写入文件
    fw.close()
    return str(user_no)


# 登录验证
def loginCheck(user_no, pwd):
    try:
        fw = open(user_file, "rb")
        users = cPickle.load(fw)
        fw.close()
    except IOError:
        users = {}
    logger.info(u"用户登录验证 {} {}".format(user_no, pwd))
    user_no = string.atoi(user_no)
    if user_no in users.keys() and users[user_no][2] == pwd:
        ret = users[user_no][1]  # "LOGIN SUCCESS"
    else:
        ret = "LOGIN FAIL"
    return u"{}".format(ret)
