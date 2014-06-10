import os
import sys
import struct
import socket
import threading
import md5

#解决发送中文异常
reload(sys)
sys.setdefaultencoding("utf-8")

PORT = 6677
DGRAM_FORMAT = "50s50s50s200s"

'''建立和服务器的连接，用于发送消息和文件'''
def connServer(srv_ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((srv_ip, PORT))
        return sock
    except Exception as e:
        return None

'''注册新用户'''
def signIn(srv_ip, email, nick, pwd):
    sock = connServer(srv_ip)
    if not sock:
        return
    pwd_md5 = md5.new(pwd).hexdigest()
    data_type = "SIGN_IN"
    data=struct.pack(DGRAM_FORMAT,data_type,str(email),str(nick),str(pwd_md5))
    sock.send(data)
    ret = sock.recv(1024)
    sock.close()
    return ret
'''登录'''
def login(srv_ip, usr_no, pwd):
    sock = connServer(srv_ip)
    if not sock:
        return
    pwd_md5 = md5.new(pwd).hexdigest()
    data_type = "LOGIN"
    data=struct.pack(DGRAM_FORMAT,data_type,str(usr_no),str(pwd_md5),"")
    sock.send(data)
    sock.settimeout(20)
    ret = None
    ret = sock.recv(1024)
    sock.close()
    return ret

'''获取好友列表,返回一个字典{user_no:nickname}'''
def getFriends(user_no,srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = "GET_FRIENDS"
    data=struct.pack(DGRAM_FORMAT,data_type,str(user_no),"","")
    sock.send(data)
    ret = sock.recv(2048)
    sock.close()
    ret = ret.split("|")
    
    if ret[0]!='OK':
        return "NULL"
    friends={}
    i = 1
    for i in range(1,len(ret),2):
        friends[ret[i]]=ret[i+1]
    return friends
'''获得所有在线的用户OC号，结合getFriends使用'''
def getOnlineUsers(srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = "GET_ONLINE"
    data=struct.pack(DGRAM_FORMAT,data_type,"","","")
    sock.send(data)
    ret = sock.recv(2048)
    sock.close()
    ret = ret.split('|')
    if ret[0]=='OK':
        return ret[1:]
    return "NULL"
'''根据OC号码查找用户'''
def find(user_no,srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = "FIND_FRIEND"
    data=struct.pack(DGRAM_FORMAT,data_type,str(user_no),"","")
    sock.send(data)
    ret = sock.recv(1024)
    sock.close()
    return u"%s" %ret
'''根据OC号码添加好友'''
def addFriend(user_no, friend_no, srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = "ADD_FRIEND"
    data=struct.pack(DGRAM_FORMAT,data_type,str(user_no),str(friend_no),"")
    sock.send(data)
    ret = sock.recv(1024)
    sock.close()
    return u"%s" %ret

'''建立会话'''
def newSession(user_no,friend_no,srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = "NEW_SESSION"
    data=struct.pack(DGRAM_FORMAT,data_type,str(user_no),str(friend_no),"")
    sock.send(data)
    return sock

'''发送消息，格式: MESG / recv_no /content'''
def sendMsg(sock,from_no,recv_no, msg):
    data = struct.pack(DGRAM_FORMAT,"MESG",str(from_no),str(recv_no),str(msg))
    sock.send(data)

'''退出时，发送下线通知'''
def notifyDown(user_no,srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = "DOWN"
    data=struct.pack(DGRAM_FORMAT,data_type,str(user_no),"","")
    sock.send(data)
    sock.close()
'''获取离线消息，一次取得一个会话的离线消息'''
def getOfflineMsg(user_no,srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = "OFFLINE_MSG"
    data=struct.pack(DGRAM_FORMAT,data_type,str(user_no),"","")
    sock.send(data)
    data = sock.recv(2048)
    sock.close()
    msg = data.split('|')
    if msg[0]=="NONE":
        print u"没有离线消息"
        return
    return msg
'''上传文件'''
def sendFile(send_no, recv_no, file_name, srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    fname = os.path.split(str(file_name))[1]
    data_type = "UPLOAD"
    data=struct.pack(DGRAM_FORMAT,data_type,str(send_no),str(recv_no),str(fname))
    sock.send(data)
    reply = sock.recv(1024)
    if reply=="RECV_NOTICE":
        fr = open(file_name,"rb")
        data = fr.read(200)
        reply = "RECV_OK"
        while len(data) > 0 and reply=="RECV_OK":
            data = struct.pack(DGRAM_FORMAT,data_type,str(len(data)),str(fname),data)
            sock.send(data)
            reply = sock.recv(1024)
            data = fr.read(200)
        fr.close()
        sock.send(struct.pack(DGRAM_FORMAT,"UPLOAD_FINISH",str(send_no),str(recv_no),str(fname)))
    sock.close()
    print u"上传成功"
    return u"上传成功"

'''获取可下载的文件列表'''
def getFileLists(send_no, recv_no, srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = 'DOWN_FILE_NAME'
    data=struct.pack(DGRAM_FORMAT,data_type,str(send_no),str(recv_no),"")
    sock.send(data)
    print sock.getsockname(),"before"
    reply = sock.recv(2048)
    print sock.getpeername(),"after"
    reply = reply.split('|')
    fnames = [fname.strip('\n') for fname in reply]
    sock.close()
    return fnames
'''下载文件'''
def recvFile(save_file_name, down_file_name, srv_ip):
    sock = connServer(srv_ip)
    if not sock:
        return
    data_type = "DOWNLOAD"
    data=struct.pack(DGRAM_FORMAT,data_type,str(down_file_name),"RECV_OK","0")
    sock.send(data)

    fw = open(save_file_name,"wb")
    recv_bytes = 0
    data=sock.recv(1024)
    while data != "FILE_END\r\n":
        fw.write(data)
        recv_bytes += len(data)
        sdata=struct.pack(DGRAM_FORMAT,data_type,str(down_file_name),"RECV_OK",str(recv_bytes))
        sock.send(sdata)
        data = sock.recv(1024)
    fw.close()
    sock.close()
    print u"下载 成功"
    return u"下载成功"
if __name__=='__main__':
    print signIn("127.0.0.1", "test@123.com","亮剑","12346")
