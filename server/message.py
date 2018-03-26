# -*- coding: utf-8 -*-

import cPickle
from const import history_msg_file, offline_msg_file
from utils import curTime


def write2file(send_uid, recv_uid, msg):
    fw = open(history_msg_file, "a")
    text = "{}\t{}\t{}\t{}".format(send_uid, recv_uid, curTime(), msg)
    cPickle.dump(text, fw)
    fw.close()


def saveOfflineMsg(send_uid, recv_uid, msg):
    fw = open(offline_msg_file, "a")
    text = "{}\t{}\t{}\t{}".format(send_uid, recv_uid, curTime(), msg)
    cPickle.dump(text, fw)
    fw.close()


def getOfflineMsg(uid):
    fr = open(offline_msg_file, "r")
    left_msg = []
    ret_msg = ""
    try:
        send_uid = ""
        line = cPickle.load(fr)
        while len(line) > 0:
            msg = line.split('\t')
            if msg[1] == uid:
                if len(send_uid) == 0:
                    send_uid = msg[0]
                if msg[0] == send_uid:
                    ret_msg = u'{}|{}|{}'.format(ret_msg, msg[2], msg[3])
                    write2file(send_uid, uid, msg[3])  # 写入history.pk
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
    if len(send_uid) > 0:
        return send_uid+ret_msg
    else:
        return "NONE"
