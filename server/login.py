from random import randint
import md5
import cPickle
import string

user_file="user\\user.pk"

#注册新用户，生成一个6位数的数字串
def register(email,nickname,pwd):
    try:
        fr = open(user_file,"rb")
        users=cPickle.load(fr)
        
        user_no = randint(100000,1000000)
        while user_no in users.keys():
            user_no = randint(100000,1000000)
        fr.close()
    except IOError or EOFError as e:
        print e
        users = {}
        user_no = randint(100000,1000000)
    #添加用户
    fw = open(user_file,"wb")
    fw.truncate()
    users[user_no]=[email,nickname,pwd]
    cPickle.dump(users,fw)#重新写入文件
    fw.close()
    return user_no

#登录验证
def loginCheck(user_no,pwd):
    try:
        fw = open(user_file,"rb")
        users=cPickle.load(fw)
    except IOError as e:
        users = {}
    print u"用户登录验证",user_no,pwd
    user_no = string.atoi(user_no)
    if user_no in users.keys() and users[user_no][2]==pwd:
        ret = users[user_no][1] #"LOGIN SUCCESS"
    else:
        ret = "LOGIN FAIL"
    fw.close()
    return u"%s" %ret
