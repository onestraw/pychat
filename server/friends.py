# -*- coding: utf-8 -*-

import cPickle
import string

user_file = "user\\user.pk"
friend_file = "user\\friends.pk"


def addFriend(user_no, friend_no):
    friends = {}
    try:
        # 判断该号码是否在在
        fr = open(user_file, "rb")
        users = cPickle.load(fr)
        fr.close()
        if string.atoi(user_no) not in users.keys() or \
           string.atoi(friend_no) not in users.keys():
            return u"号码为空"
        # 判断是否已为好友
        fr = open(friend_file, "rb")
        friends = cPickle.load(fr)
        fr.close()
        if user_no in friends and friend_no in friends[user_no]:
            return u"你们已经是好友啦"
    except IOError:
        pass
    except EOFError:
        pass

    # 添加用户
    fw = open(friend_file, "wb")
    fw.truncate()
    if user_no not in friends.keys():
        friends[user_no] = []
    friends[user_no].append(friend_no)
    cPickle.dump(friends, fw)  # 重新写入文件
    fw.close()
    return "ADD_SUCCESS"


def findFriend(user_no):
    try:
        fr = open(user_file, "rb")
        users = cPickle.load(fr)
        fr.close()
        user_no = string.atoi(user_no)
        if user_no in users.keys():
            return u"[{}]{}".format(users[user_no][1], users[user_no][0])
        else:
            return u"号码为空"
    except IOError or EOFError as e:
        return str(e)


def getFriends(user_no):
    try:
        fr = open(friend_file, "rb")
        friends = cPickle.load(fr)
        fr.close()
        # 将user_no的所有好友信息(no+nickname)连接成一个字符串，返回给客户端
        ret = "OK"
        if user_no in friends.keys():
            fp = open(user_file, "rb")
            users = cPickle.load(fp)
            fp.close()
            for fno in friends[user_no]:
                nickname = u"{}".format(users[string.atoi(fno)][1])
                ret = ret+"|"+fno+"|"+nickname
            return ret
        else:
            return u"号码为空"
    except IOError or EOFError as e:
        return str(e)
