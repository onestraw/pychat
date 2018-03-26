# -*- coding: utf-8 -*-

import os
from const import FILE_PATH, file_info
from utils import curTime


def file_path(fname):
    return os.path.join(FILE_PATH, fname)


def recordFileInfo(send_uid, recv_uid, fname):
    fw = open(file_info, "a")
    cont = u"{}\t{}\t{}\t{}\n".format(send_uid, recv_uid, curTime(), fname)
    fw.write(cont)
    fw.close()


def write2file(fname, cont):
    fw = open(file_path(fname), "ab")
    fw.write(cont)
    fw.close()


def getFileLists(send_uid, recv_uid):
    ret = ""
    fr = open(file_info, "r")
    line = fr.readline()
    while len(line) > 2:
        fields = line.split('\t')
        if (fields[0] == send_uid and fields[1] == recv_uid) or \
                (fields[1] == send_uid and fields[0] == recv_uid):
            ret = ret + "|" + fields[3]
        line = fr.readline()
    fr.close()
    if len(ret) == 0:
        ret = "NONE"
    return ret


def getFileContent(fname, recvd_bytes, read_bytes):
    fr = open(file_path(fname), "rb")
    fr.seek(recvd_bytes)
    rdata = fr.read(read_bytes)
    fr.close()
    return rdata
