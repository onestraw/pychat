﻿# -*- coding: utf-8 -*-

import cPickle
import time
from const import history_msg_file, offline_msg_file


def curTime():
    return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


def write2file(send_user_no, recv_user_no, msg):
    fw = open(history_msg_file, "a")
    text = "{}\t{}\t{}\t{}".format(send_user_no, recv_user_no, curTime(), msg)
    cPickle.dump(text, fw)
    fw.close()


def saveOfflineMsg(send_user_no, recv_user_no, msg):
    fw = open(offline_msg_file, "a")
    text = "{}\t{}\t{}\t{}".format(send_user_no, recv_user_no, curTime(), msg)
    cPickle.dump(text, fw)
    fw.close()


def getOfflineMsg(uno):
    fr = open(offline_msg_file, "r")
    left_msg = []
    ret_msg = ""
    try:
        send_no = ""
        line = cPickle.load(fr)
        while len(line) > 0:
            msg = line.split('\t')
            if msg[1] == uno:
                if len(send_no) == 0:
                    send_no = msg[0]
                if msg[0] == send_no:
                    ret_msg = u'{}|{}|{}'.format(ret_msg, msg[2], msg[3])
                    write2file(send_no, uno, msg[3])  # 写入history.pk
                else:
                    left_msg.append(line)
            else:
                left_msg.append(line)
            line = cPickle.load(fr)

    except EOFError:
        pass
    fr.close()
    fw = open(offline_msg_file, "w")
    fw.truncate()
    for line in left_msg:
        cPickle.dump(line, fw)
    fw.close()
    if len(send_no) > 0:
        return send_no+ret_msg
    else:
        return "NONE"
