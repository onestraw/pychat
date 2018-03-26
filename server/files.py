# -*- coding: utf-8 -*-

import os
import time
from const import FILE_PATH, file_info


def file_path(fname):
    return os.path.join(FILE_PATH, fname)


def curTime():
    return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


def recordFileInfo(sno, rno, fname):
    fw = open(file_info, "a")
    cont = u"{}\t{}\t{}\t{}\n".format(sno, rno, curTime(), fname)
    fw.write(cont)
    fw.close()


def write2file(fname, cont):
    fw = open(file_path(fname), "ab")
    fw.write(cont)
    fw.close()


def getFileLists(sno, rno):
    ret = ""
    fr = open(file_info, "r")
    line = fr.readline()
    while len(line) > 2:
        fields = line.split('\t')
        if (fields[0] == sno and fields[1] == rno) or \
                (fields[1] == sno and fields[0] == rno):
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
