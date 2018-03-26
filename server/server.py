# -*- coding: utf-8 -*-

import sys
import string
import socket
import select
import Queue
import struct
import argparse
from daemon import Daemon

import friends
import login
import message
import files
from logger import logger
from const import IP, PORT, DGRAM_FORMAT, CMD_FORMAT, PID_FILE

# 解决发送中文异常
reload(sys)
sys.setdefaultencoding('utf-8')


class Server(Daemon):
    def __init__(self, pidfile, ip='', port=6677):
        super(Server, self).__init__(pidfile)
        self.ip = ip
        self.port = port
        self.listenNum = 50
        self.runFlag = 1
        self.onlineUser = []
        self.sessions = {}    # 这里保存的socket用于传输消息
        self.cmd_sock = {}    # 每个客户端用于接收推送消息的cmd socket

    def run(self):
        self.sock = self.newSocket()
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
                    logger.info('connection from {}'.format(cli_addr))
                    inputs.append(conn)
                    msgQueues[conn] = Queue.Queue()
                else:  # connection is created
                    data = s.recv(1024)
                    if data:
                        raw_fields = struct.unpack(DGRAM_FORMAT, data)
                        fields = [e.strip('\x00') for e in raw_fields]
                        a, b, c, d = fields
                        logger.debug('recv {} from {}'.format('#'.join(fields),
                                     s.getpeername()))

                        # 注册新用户
                        if a == 'SIGN_IN':
                            uid = login.register(b, c, d)
                            logger.info(u'随机生成一个OC号: {}'.format(uid))
                            msgQueues[s].put(uid)
                            friends.addFriend(uid, uid)

                        # 登录验证
                        elif a == 'LOGIN':
                            uid, pwd = b, c
                            reply = login.loginCheck(uid, pwd)
                            msgQueues[s].put(reply)
                            if reply != 'LOGIN FAIL':   # 登录成功
                                self.onlineUser.append(uid)
                                msg = struct.pack(CMD_FORMAT, 'UP', uid, '')
                                for kno in self.cmd_sock:
                                    if self.cmd_sock[kno] in msgQueues:
                                        msgQueues[self.cmd_sock[kno]].put(msg)

                        # 客户端下线通知
                        elif a == 'DOWN':
                            uid = b
                            logger.info(u'{} 下线通知'.format(uid))
                            if uid in self.onlineUser:
                                self.onlineUser.remove(uid)
                            if uid in self.sessions:
                                for fid in self.sessions[uid]:
                                    usock = self.sessions[uid][fid]
                                    if usock:
                                        usock.close()
                                self.sessions.pop(uid)

                            sdata = struct.pack(CMD_FORMAT, 'DOWN', uid, '')
                            for kno in self.cmd_sock:
                                if self.cmd_sock[kno] in msgQueues:
                                    msgQueues[self.cmd_sock[kno]].put(sdata)

                        # 每个客户端一个cmd socket
                        elif a == 'CMD_SOCKET':
                            uid = b
                            self.cmd_sock[uid] = s

                        # 查找好友列表，返回uid, nickname
                        elif a == 'GET_FRIENDS':
                            reply = friends.getFriends(b)
                            msgQueues[s].put(reply)

                        # 获取当前在线的所账号
                        elif a == 'GET_ONLINE':
                            ou = '|'.join(self.onlineUser)
                            reply = 'OK|' + ou
                            msgQueues[s].put(reply)

                        # 查找好友
                        elif a == 'FIND_FRIEND':
                            reply = friends.findFriend(b)
                            msgQueues[s].put(reply)

                        # 添加好友，双向添加，默认不提示被动添加的一方
                        elif a == 'ADD_FRIEND':
                            uid, fid = b, c

                            reply = friends.addFriend(uid, fid)
                            if reply == 'ADD_SUCCESS':
                                reply = friends.addFriend(fid, uid)
                                ret = friends.findFriend(fid)
                                fnick = ret.split('[')[1].split(']')[0]
                                state = 'OFFLINE'
                                if fid in self.onlineUser:
                                    state = 'ONLINE'

                                reply = u'{}|{}|{}'.format(fid, fnick, state)
                                msgQueues[s].put(reply)
                            else:
                                msgQueues[s].put(reply)

                        # 查找离线消息，返回send_uid, msg
                        elif a == 'OFFLINE_MSG':
                            uid = b
                            sdata = message.getOfflineMsg(uid)
                            logger.info(u'离线消息:{}'.format(sdata))
                            msgQueues[s].put(sdata)

                        # 建立会话、或接收会话
                        elif a == 'NEW_SESSION':
                            uid, fid = b, c
                            if uid not in self.sessions.keys():
                                self.sessions[uid] = {}
                            self.sessions[uid][fid] = s
                            logger.info('new session between {} and {}'.format(uid, fid))

                        # 转发消息
                        elif a == 'MESG':
                            uid, fid, msg = b, c, d
                            logger.info(u'to {}: {}'.format(fid, msg))
                            if fid not in self.onlineUser:
                                # 写入离线消息文件，并提示
                                message.saveOfflineMsg(uid, fid, msg)
                                msg = u'{}处于离线状态!'.format(fid)
                                msgQueues[self.sessions[uid][fid]].put(msg)
                            else:
                                # 如果fid和uid还没有建立会话，那么先建立socket
                                if fid not in self.sessions.keys() or \
                                        uid not in self.sessions[fid].keys():
                                    fsock = self.cmd_sock[fid]
                                    logger.info('... cmd socket {} {}'.format(
                                                fid, fsock.getpeername()))
                                    sdata = struct.pack(CMD_FORMAT,
                                                        'NEW_SESSION',
                                                        str(uid),
                                                        msg)
                                    msgQueues[fsock].put(sdata)
                                    logger.debug('MESG....deubg')
                                else:
                                    msgQueues[self.sessions[fid][uid]].put(msg)

                                message.write2file(uid, fid, msg)

                        # 上传文件
                        elif a == 'UPLOAD':
                            if len(b) == 6 and len(c) == 6:  # todo: 区分upload cmd和data
                                send_uid, recv_uid, filename = b, c, d
                                msgQueues[self.sessions[send_uid][recv_uid]].\
                                    put(u'正在上传...')

                                msgQueues[s].put('RECV_NOTICE')
                                files.recordFileInfo(send_uid, recv_uid, filename)
                            else:
                                datalen = string.atoi(b)
                                filename, content = c, raw_fields[-1]
                                files.write2file(filename, content[0:datalen])
                                msgQueues[s].put('RECV_OK')

                        # 上传完成
                        elif a == 'UPLOAD_FINISH':
                            send_uid, recv_uid, filename = b, c, d

                            if recv_uid in self.sessions and \
                                    send_uid in self.sessions[recv_uid]:
                                sdata = u'FILE\r\n{}|{}'.format(send_uid, filename)
                                msgQueues[self.sessions[recv_uid][send_uid]].put(sdata)
                            elif recv_uid in self.onlineUser:
                                fsock = self.cmd_sock[recv_uid]
                                logger.info('... cmd socket {} {}'.format(
                                            recv_uid, fsock.getpeername()))
                                msg = u'{}正在向你传送文件:{}'.format(send_uid, filename)
                                sdata = struct.pack(CMD_FORMAT, 'NEW_SESSION',
                                                    send_uid, str(msg))
                                msgQueues[fsock].put(sdata)
                                logger.debug('FILE....deubg')

                        # 可以下载的离线文件
                        elif a == 'DOWN_FILE_NAME':
                            fs = files.getFileLists(b, c)
                            msgQueues[s].put(fs)
                        elif a == 'DOWNLOAD':
                            filename, status, size = b, c, d
                            recvd_bytes = string.atoi(size)
                            if status == 'RECV_OK':
                                rdata = files.getFileContent(filename, recvd_bytes, 1024)
                                if len(rdata) < 1:
                                    rdata = 'FILE_END\r\n'
                                msgQueues[s].put(rdata)

                        if s not in outputs:
                            outputs.append(s)
                    else:   # data is None
                        logger.info(u'关闭socket: {}'.format(s.getpeername()))
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
                logger.error('exceptional condition on {}'.format(s.getpeername()))
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del msgQueues[s]

    def newSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen(self.listenNum)
        return sock


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pychat server')
    parser.add_argument('--action', dest='action', default='start',
                        help='start/stop (default: %(default)s)')
    parser.add_argument('--pidfile', dest='pidfile',
                        default=PID_FILE,
                        help='pidfile (default: %(default)s)')
    args = parser.parse_args()

    s = Server(args.pidfile, IP, PORT)
    if args.action == 'start':
        logger.info('server is starting')
        s.start()
    elif args.action == 'stop':
        s.stop()
        logger.info('server is stopped')
    else:
        raise Exception('arguments error')
