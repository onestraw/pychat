# -*- coding: utf-8 -*-

import sys
import string
import socket
import select
import Queue
import struct
from threading import Thread

import friends
import login
import message
import files

# 解决发送中文异常
reload(sys)
sys.setdefaultencoding("utf-8")


IP = "127.0.0.1"
PORT = 6677
DGRAM_FORMAT = "50s50s50s200s"


def _strip(s):
    return s.strip('\x00')


class Server(Thread):
    def __init__(self, ip="", port=6677):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.listenNum = 50
        self.sock = self.newSocket()
        self.runFlag = 1
        self.onlineUser = []
        self.sessions = {}    # 这里保存的socket用于传输消息
        self.cmd_sock = {}    # 每个客户端用于接收推送消息的cmd socket

    def run(self):
        inputs = [self.sock]
        outputs = []
        msgQueues = {}
        while self.runFlag:
            readable, writable, exceptional = \
                    select.select(inputs, outputs, inputs, 0.1)

            for s in readable:
                if s is self.sock:
                    conn, cli_addr = s.accept()
                    conn.setblocking(0)
                    print('connection from {}'.format(cli_addr))
                    inputs.append(conn)
                    msgQueues[conn] = Queue.Queue()
                else:  # connection is created
                    data = s.recv(1024)
                    if data:
                        print('recv {} from {}'.format(data, s.getpeername()))
                        a, b, c, d = struct.unpack(DGRAM_FORMAT, data)
                        a = a.strip("\x00")
                        # 注册新用户
                        if a == 'SIGN_IN':
                            user_no = login.register(_strip(b),
                                                     _strip(c), _strip(d))
                            print(u"随机生成一个OC号: {}".format(user_no))
                            user_no = str(user_no)
                            msgQueues[s].put(user_no)
                            friends.addFriend(user_no, user_no)

                        # 登录验证
                        elif a == 'LOGIN':
                            uno = _strip(b)
                            reply = login.loginCheck(uno, _strip(c))
                            msgQueues[s].put(reply)
                            if reply != "LOGIN FAIL":   # 登录成功
                                self.onlineUser.append(uno)
                                msg = struct.pack("50s50s50s", "UP", uno, "")
                                for kno in self.cmd_sock:
                                    if self.cmd_sock[kno] in msgQueues:
                                        msgQueues[self.cmd_sock[kno]].put(msg)

                        # 客户端下线通知
                        elif a == 'DOWN':
                            uno = _strip(b)
                            print(u"%s下线通知{}".format(uno))
                            if uno in self.onlineUser:
                                self.onlineUser.remove(uno)
                            if uno in self.sessions:
                                for fno in self.sessions[uno]:
                                    usock = self.sessions[uno][fno]
                                    if usock:
                                        usock.close()
                                self.sessions.pop(uno)

                            sdata = struct.pack("50s50s50s", "DOWN", uno, "")
                            for kno in self.cmd_sock:
                                if self.cmd_sock[kno] in msgQueues:
                                    msgQueues[self.cmd_sock[kno]].put(sdata)

                        # 每个客户端一个cmd socket
                        elif a == 'CMD_SOCKET':
                            uno = _strip(b)
                            self.cmd_sock[uno] = s

                        # 查找好友列表，返回user_no, nickname
                        elif a == 'GET_FRIENDS':
                            reply = friends.getFriends(_strip(b))
                            msgQueues[s].put(reply)

                        # 获取当前在线的所账号
                        elif a == 'GET_ONLINE':
                            ou = '|'.join(self.onlineUser)
                            reply = "OK" + ou

                            msgQueues[s].put(reply)

                        # 查找好友
                        elif a == 'FIND_FRIEND':
                            reply = friends.findFriend(_strip(b))
                            msgQueues[s].put(reply)

                        # 添加好友，双向添加，默认不提示被动添加的一方
                        elif a == 'ADD_FRIEND':
                            uno = _strip(b)
                            fno = _strip(c)

                            reply = friends.addFriend(fno, uno)
                            reply = friends.addFriend(uno, fno)
                            if reply == 'ADD_SUCCESS':
                                ret = friends.findFriend(fno)
                                fnick = ret.split('[')[1].split(']')[0]
                                state = "OFFLINE"
                                if fno in self.onlineUser:
                                    state = 'ONLINE'

                                reply = u"{}|{}|{}".format(fno, fnick, state)
                                msgQueues[s].put(reply)

                        # 查找离线消息，返回send_user_no, msg
                        elif a == 'OFFLINE_MSG':
                            uno = _strip(b)
                            sdata = message.getOfflineMsg(uno)
                            print(u"离线消息:{}".format(sdata))
                            msgQueues[s].put(sdata)

                        # 建立会话、或接收会话
                        elif a == 'NEW_SESSION':
                            user_no = _strip(b)
                            friend_no = _strip(c)
                            if user_no not in self.sessions.keys():
                                self.sessions[user_no] = {}
                            self.sessions[user_no][friend_no] = s
                            print("new session between {} and {}".format(
                                user_no, friend_no))

                        # 转发消息
                        elif a == 'MESG':
                            uno = _strip(b)
                            fno = _strip(c)
                            msg = _strip(d)
                            print(u"to {}: {}".format(fno, msg))
                            if fno not in self.onlineUser:
                                # 写入离线消息文件，并提示
                                message.saveOfflineMsg(uno, fno, msg)
                                msg = u"{}处于离线状态!".format(fno)
                                msgQueues[self.sessions[uno][fno]].put(msg)
                            else:
                                # 如果fno和uno还没有建立会话，那么先建立socket
                                if fno not in self.sessions.keys() or \
                                        uno not in self.sessions[fno].keys():
                                    fsock = self.cmd_sock[fno]
                                    print("... cmd socket {} {}".format(
                                        fno, fsock.getpeername()))
                                    sdata = struct.pack("50s50s50s",
                                                        "NEW_SESSION",
                                                        str(uno),
                                                        msg)
                                    msgQueues[fsock].put(sdata)
                                    print("MESG....deubg")
                                else:
                                    msgQueues[self.sessions[fno][uno]].put(msg)

                                message.write2file(uno, fno, msg)

                        # 上传文件
                        elif a == 'UPLOAD':
                            b = _strip()
                            if len(b) == 6:
                                sno = _strip(b)
                                rno = _strip(c)
                                fname = _strip(d)
                                msgQueues[self.sessions[sno][rno]].put(
                                        u"正在上传...")

                                msgQueues[s].put("RECV_NOTICE")
                                files.recordFileInfo(sno, rno, fname)
                            else:
                                dlen = string.atoi(b)
                                fname = _strip(c)
                                cont = d
                                files.write2file(fname, cont[0:dlen])
                                msgQueues[s].put("RECV_OK")

                        # 上传完成
                        elif a == 'UPLOAD_FINISH':
                            sno = _strip(b)
                            rno = _strip(c)
                            fname = _strip(d)
                            if rno in self.sessions and \
                                    sno in self.sessions[rno]:
                                sdata = u"FILE\r\n{}|{}".format(sno, fname)
                                msgQueues[self.sessions[rno][sno]].put(sdata)
                            elif rno in self.onlineUser:
                                fsock = self.cmd_sock[rno]
                                print("... cmd socket {} {}".format(
                                    rno, fsock.getpeername()))
                                msg = u"{}正在向你传送文件:{}".format(sno, fname)
                                sdata = struct.pack("50s50s50s", "NEW_SESSION",
                                                    str(sno), str(msg))
                                msgQueues[fsock].put(sdata)
                                print("FILE....deubg")

                        # 可以下载的离线文件
                        elif a == 'DOWN_FILE_NAME':
                            fnames = files.getFileLists(_strip(b), _strip(c))
                            msgQueues[s].put(fnames)
                        elif a == 'DOWNLOAD':
                            fname = _strip(b)
                            recvd_bytes = string.atoi(d.strip('\x00'))
                            if _strip(c) == "RECV_OK":
                                rdata = files.getFileContent(
                                        fname, recvd_bytes, 1024)
                                if len(rdata) < 1:
                                    rdata = 'FILE_END\r\n'
                                msgQueues[s].put(rdata)

                        if s not in outputs:
                            outputs.append(s)
                    else:   # data is None
                        print(u"关闭socket: ", s.getpeername())
                        if s in outputs:
                            outputs.remove(s)
                        for k1 in self.sessions.keys():
                            for k2 in self.sessions[k1].keys():
                                if self.sessions[k1][k2] == s:
                                    self.sessions[k1].pop(k2)
                                    break
                        inputs.remove(s)
                        s.close()
                        del msgQueues[s]

            for s in writable:
                if s not in msgQueues:
                    continue
                try:
                    nextMsg = msgQueues[s].get_nowait()
                    s.send(nextMsg)
                except Queue.Empty:
                    pass

            for s in exceptional:
                print("exceptional condition on {}".format(s.getpeername()))
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del msgQueues[s]

    def stop(self):
        self.runFlag = 0
        if self.sock:
            self.sock.close()

    def newSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen(self.listenNum)
        return sock


if __name__ == '__main__':
    try:
        s = Server(IP, PORT)
        s.start()
    except KeyboardInterrupt:
        s.stop()
        print("CTRL+Z/D, server end")
