# -*- coding: utf-8 -*-

import cPickle
import string
from const import user_file, friend_file


def addFriend(uid, friend_uid):
    friends = {}
    try:
        # 判断该号码是否在在
        fr = open(user_file, "rb")
        users = cPickle.load(fr)
        fr.close()
        if string.atoi(uid) not in users.keys() or \
           string.atoi(friend_uid) not in users.keys():
            return u"号码为空"
        # 判断是否已为好友
        fr = open(friend_file, "rb")
        friends = cPickle.load(fr)
        fr.close()
        if uid in friends and friend_uid in friends[uid]:
            return u"你们已经是好友啦"
    except IOError:
        pass
    except EOFError:
        pass

    # 添加用户
    fw = open(friend_file, "wb")
    fw.truncate()
    if uid not in friends.keys():
        friends[uid] = []
    friends[uid].append(friend_uid)
    cPickle.dump(friends, fw)  # 重新写入文件
    fw.close()
    return "ADD_SUCCESS"


def findFriend(uid):
    try:
        fr = open(user_file, "rb")
        users = cPickle.load(fr)
        fr.close()
        uid = string.atoi(uid)
        if uid in users.keys():
            return u"[{}]{}".format(users[uid][1], users[uid][0])
        else:
            return u"号码为空"
    except IOError or EOFError as e:
        return str(e)


def getFriends(uid):
    try:
        fr = open(friend_file, "rb")
        friends = cPickle.load(fr)
        fr.close()
        # 将uid的所有好友信息(uid+nickname)连接成一个字符串，返回给客户端
        ret = "OK"
        if uid in friends.keys():
            fp = open(user_file, "rb")
            users = cPickle.load(fp)
            fp.close()
            for fid in friends[uid]:
                nickname = u"{}".format(users[string.atoi(fid)][1])
                ret = ret+"|"+fid+"|"+nickname
            return ret
        else:
            return u"号码为空"
    except IOError or EOFError as e:
        return str(e)
