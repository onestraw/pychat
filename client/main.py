# -*- coding: utf-8 -*-

import sys
import time
import socket
import struct
import Queue
import select
import threading
import net

from PyQt4 import QtCore, QtGui

from ui_login import Ui_DialogLogin
from ui_register import Ui_DialogRegister
from ui_main import Ui_MainWindow
from ui_chat import Ui_DialogChat

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class LoginDialog(QtGui.QDialog):
    # 登录对话框
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DialogLogin(self)
        self.ui.lineEdit_srv.setText("127.0.0.1")
        self.ui.lineEdit_usr.setText("347473")
        self.ui.lineEdit_pas.setText("123456")
        self.setup()

    def setup(self):
        # self.ui.Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowSystemMenuHint)
        QtCore.QObject.connect(self.ui.pushButton_log,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.login)
        QtCore.QObject.connect(self.ui.pushButton_reg,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.openRegDlg)

    def login(self):
        srv_ip = self.ui.lineEdit_srv.text()
        user_no = self.ui.lineEdit_usr.text()
        pwd = self.ui.lineEdit_pas.text()
        if not srv_ip or not user_no or not pwd:
            self.ui.label_error.setText(u"没有输入用户名或密码")
            return
        # 将user_no和pwd发送到srv_ip进行验证
        self.ui.label_error.setText(u"正在登录...")
        msg = net.login(srv_ip, user_no, pwd)
        if not msg or msg == 'LOGIN FAIL':
            msg = u"登录失败，请重试"
            self.ui.label_error.setText(msg)
        else:
            self.accept()
            mainWin = MainWindow(srv_ip, user_no, msg)
            mainWin.show()

    def openRegDlg(self):
        print "register..."
        regDlg = RegisterDialog()
        regDlg.exec_()
        regDlg.destroy()


class RegisterDialog(QtGui.QDialog):
    # 注册对话框
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DialogRegister(self)
        self.ui.lineEdit_srv.setText("127.0.0.1")
        self.setup()

    def setup(self):
        QtCore.QObject.connect(
                self.ui.pushButton_reg,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                self.register)

    def register(self):
        srv_ip = self.ui.lineEdit_srv.text()
        email = self.ui.lineEdit_eml.text()
        nick = self.ui.lineEdit_usr.text()
        pwd = self.ui.lineEdit_pas.text()
        if not srv_ip or not nick or not pwd or not email:
            self.ui.label_error.setText(u"请填写完整!")
            return

        # 将email、nick和pwd发送到srv_ip进行注册，返回一个OC数字号码
        self.ui.label_error.setText(u"正在注册...")
        no = net.signIn(srv_ip, email, nick, pwd)
        msg = u"你的OC号为:%s" % no
        self.ui.label_error.setText(msg)


class T(QtCore.QObject, threading.Thread):
    '''
    GUI线程
    GUI进程的子线程不能调用GUI控件
    '''
    signal_up = QtCore.pyqtSignal()
    signal_down = QtCore.pyqtSignal()
    signal_session = QtCore.pyqtSignal()

    def __init__(self, srv_ip, user_no, parent=None):
        threading.Thread.__init__(self)
        super(T, self).__init__(parent)
        self.runFlag = 1
        self.sock = net.connServer(srv_ip)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cmd_data = struct.pack(
                net.DGRAM_FORMAT, "CMD_SOCKET", str(user_no), "", "")
        self.sock.send(cmd_data)
        self.fno = ""
        self.msg = ""
        print "thread running"

    def run(self):
        while self.runFlag:
            inputready, outputready, exceptready = \
                    select.select([self.sock], [], [self.sock], 0.1)
            for s in inputready:
                data = s.recv(1024)
                print "cmd threading debuging\n\n"
                mtype, fno, msg = struct.unpack("50s50s50s", data)
                mtype = mtype.strip('\x00')
                self.fno = fno.strip('\x00')
                self.msg = msg.strip("\x00")
                if mtype == 'UP':
                    print self.fno, ' UP'
                    self.signal_up.emit()
                elif mtype == 'DOWN':
                    print self.fno, "dwon notify"
                    self.signal_down.emit()
                elif mtype == 'NEW_SESSION':
                    print self.fno, "session request"
                    self.signal_session.emit()
        self.sock.close()
        print "thread ending .close socket"

    def stop(self):
        self.runFlag = 0


class T2(QtCore.QObject, threading.Thread):
    '''
    等待客户端启动5s后再查询有没有离线消息
    '''
    signal_queryOfflineMsg = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        threading.Thread.__init__(self)
        super(T2, self).__init__(parent)

    def run(self):
        time.sleep(5)
        self.signal_queryOfflineMsg.emit()


class MainWindow(QtGui.QMainWindow):
    # 主界面
    def __init__(self, srv_ip, user_no, nickname, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow(self)
        self.ui.label_nickname.setText("%s[%s]" % (nickname, user_no))
        self.srv_ip = srv_ip
        self.user_no = user_no
        self.nick = nickname
        self.sock = net.connServer(self.srv_ip)
        self.setupTrayIcon()
        self.friends = {}
        self.onlist = {}
        self.offlist = {}
        self.chatroom = {}
        self.root_online = {}
        self.root_offline = {}
        self.setupFriendList()
        self.setupSignals()
        self.runDlg = {}
        self._t = None
        self.cmdTread()
        # self.queryOfflineMsg()
        self._t2 = T2()
        self._t2.signal_queryOfflineMsg.connect(self.queryOfflineMsg)
        self._t2.start()

    def queryOfflineMsg(self):
        print u"查询有没有我的离线消息"
        msg = net.getOfflineMsg(self.user_no, self.srv_ip)
        print type(msg), msg
        if isinstance(msg, list):
            self.offlineMsgBox(msg[0], msg[1:])

    def cmdTread(self):
        self._t = T(self.srv_ip, self.user_no)
        self._t.signal_session.connect(self.questionMsgBox)
        self._t.signal_down.connect(self.friendDown)
        self._t.signal_up.connect(self.friendUp)
        self._t.start()

    def friendUp(self):
        fno = self._t.fno
        if fno not in self.offlist.keys():
            return
        item = self.offlist[fno]
        self.root_offline.removeChild(item)
        self.root_online.addChild(item)
        self.offlist.pop(fno)
        self.onlist[fno] = item

    def friendDown(self):
        fno = self._t.fno
        if fno not in self.onlist.keys():
            return
        item = self.onlist[fno]
        self.root_online.removeChild(item)
        self.root_offline.addChild(item)
        self.onlist.pop(fno)
        self.offlist[fno] = item

    def questionMsgBox(self):
        # 弹出接收文件消息框
        fno = self._t.fno
        first_msg = self._t.msg
        if fno not in self.friends.keys():
            return
        msg = u"%s(%s)发来了消息" % (self.friends[fno], fno)
        # print msg
        button = QtGui.QMessageBox.question(None, u"消息提醒",
                                            msg,
                                            QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if button == QtGui.QMessageBox.Yes:
            self.passiveOpenChatDlg(fno, first_msg)

    def offlineMsgBox(self, fno, msg):
        # 弹出接收离线消息框
        if fno not in self.friends.keys():
            return
        prompt = u"%s(%s)发来了消息" % (self.friends[fno], fno)
        # print msg
        button = QtGui.QMessageBox.question(None, u"消息提醒",
                                            prompt,
                                            QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if button == QtGui.QMessageBox.Yes:
            self.passiveOpenChatDlg(fno, msg)

    def closeEvent(self, event):
        net.notifyDown(self.user_no, self.srv_ip)
        if self._t:
            self._t.stop()
        if self.sock:
            self.sock.close()
        self.close()
        print u"正在退出。。。"

    def setupFriendList(self):
        tw = self.ui.treeWidget
        tw.setColumnCount(1)
        tw.setHeaderLabels([u""])
        tw.setItemsExpandable(True)

        root_online = QtGui.QTreeWidgetItem(tw)
        root_online.setText(0, u"在线好友")
        root_offline = QtGui.QTreeWidgetItem(tw)
        root_offline.setText(0, u"离线好友")
        root_chatroom = QtGui.QTreeWidgetItem(tw)
        root_chatroom.setText(0, u"聊天室")
        tw.addTopLevelItem(root_online)
        tw.addTopLevelItem(root_offline)
        tw.addTopLevelItem(root_chatroom)
        icon_on = QtGui.QIcon(":/pic/img/avatar-0.jpg")
        icon_off = QtGui.QIcon(":/pic/img/avatar-1.jpg")
        icon_cr = QtGui.QIcon(":/pic/img/avatar.jpg")
        '''
        child1 = QtGui.QTreeWidgetItem(root_online)
        child1.setText(0, u"测试用户")
        child1.setIcon(0, icon_on)
        child2 = QtGui.QTreeWidgetItem(root_offline)
        child2.setText(0, u"测试用户")
        child2.setIcon(0, icon_off)
        '''
        child3 = QtGui.QTreeWidgetItem(root_chatroom)
        child3.setText(0, u"测试聊天室")
        child3.setIcon(0, icon_cr)
        # self.onlist['0'] =child1
        # self.offlist['0'] =child2
        self.chatroom['0'] = child3
        # 在线与离线
        friends = net.getFriends(self.user_no, self.srv_ip)
        self.friends = friends
        onlineUser = net.getOnlineUsers(self.srv_ip)
        # print friends, "debug..."
        for k in friends.keys():
            if k in onlineUser:
                item = QtGui.QTreeWidgetItem(root_online)
                item.setText(0, u"%s(%s)" % (friends[k], k))
                item.setIcon(0, icon_on)
                self.onlist[k] = item
            else:
                item = QtGui.QTreeWidgetItem(root_offline)
                item.setText(0, u"%s(%s)" % (friends[k], k))
                item.setIcon(0, icon_off)
                self.offlist[k] = item
        self.ui.treeWidget.itemDoubleClicked.connect(self.openChatDlg)
        self.root_online = root_online
        self.root_offline = root_offline

    def openChatDlg(self, item, col):
        if item in self.onlist.values() or item in self.offlist.values():
            text = u"%s" % str(item.text(0))
            user_no = text.split('(')[1].split(')')[0]
            print u"open chat dialog for ", user_no
            chat_dlg = ChatDialog(self.user_no, self.nick, user_no,
                                  self.friends[user_no], self.srv_ip,
                                  parent=None)
            self.runDlg[user_no] = chat_dlg
            chat_dlg.exec_()
            chat_dlg.destroy()
            self.runDlg.pop(user_no)
            print u"关闭会话..."

    def passiveOpenChatDlg(self, user_no, msg):
        chat_dlg = ChatDialog(self.user_no, self.nick, user_no,
                              self.friends[user_no], self.srv_ip,
                              msg=msg, parent=None)
        self.runDlg[user_no] = chat_dlg
        chat_dlg.exec_()
        chat_dlg.destroy()
        self.runDlg.pop(user_no)

    def setupSignals(self):
        QtCore.QObject.connect(self.ui.pushButton_findfriend,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.find)
        QtCore.QObject.connect(self.ui.pushButton_addfriend,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.addFriend)

    def find(self):
        user_no = "%s" % self.ui.lineEdit.text()
        if len(user_no) > 0:
            ret = net.find(user_no, self.srv_ip)
        else:
            ret = u"请输入OC号"
        print "debug", ret
        self.ui.label_3.setText(ret)

    def addFriend(self):
        uno = "%s" % self.ui.lineEdit.text()
        if len(uno) > 0:
            ret = net.addFriend(self.user_no, uno, self.srv_ip)
            fields = ret.split('|')
            if len(fields) == 3:
                if fields[2] == 'ONLINE':
                    item = QtGui.QTreeWidgetItem(self.root_online)
                    self.onlist[uno] = item
                else:
                    item = QtGui.QTreeWidgetItem(self.root_offline)
                    self.offlist[uno] = item
                item.setText(0, u"%s(%s)" % (fields[1], uno))
                icon = QtGui.QIcon(":/pic/img/avatar.jpg")
                item.setIcon(0, icon)
                self.friends[uno] = fields[1]
        else:
            ret = u"请输入OC号"
        self.ui.label_3.setText(ret)

    def setupTrayIcon(self):
        # 设置系统托盘图标
        self.icon = QtGui.QIcon(':/pic/img/avatar.jpg')
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.setToolTip(u'OC聊天')
        self.trayIcon.show()
        self.trayIcon.showMessage("debug", u"托盘气泡信息")

        self.minimizeAction = QtGui.QAction(u"最小化", self, triggered=self.hide)
        self.restoreAction = QtGui.QAction(u"显示窗口", self,
                                           triggered=self.showNormal)
        self.quitAction = QtGui.QAction(u"退出", self, triggered=self.close)
        # 弹出的菜单的行为，包括退出，还原，最小化
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu)

        QtCore.QObject.connect(
            self.trayIcon,
            QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),
            self.sysTrayIcon_activated)

    def sysTrayIcon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.show()


class ChatDialog(QtGui.QDialog):
    '''聊天对话框'''
    def __init__(self, user_no, nick, fno, fnick, srv_ip, msg="", parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DialogChat(self)
        self.runFlag = 1
        self.user_no = user_no
        self.nick = nick
        self.fno = fno
        self.fnick = fnick
        self.srv_ip = srv_ip
        self.sMsgQueue = Queue.Queue()
        self.sock = net.newSession(self.user_no, self.fno, srv_ip)
        self.sock.setblocking(0)
        t = threading.Thread(target=self.session, args=(msg,))
        t.start()
        self.setupSignals()
        dlg_title = u"%s(%s)" % (self.fnick, self.fno)
        self.ui.Dialog.setWindowTitle(_translate("Dialog", dlg_title, None))
        # print "debugbug...", user_no, nick, fno, fnick
        self.show()

    def setupSignals(self):
        QtCore.QObject.connect(self.ui.sendButton,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.sendMsg)
        QtCore.QObject.connect(self.ui.sendFileButton,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.sendFileThread)
        QtCore.QObject.connect(self.ui.recvFileButton,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.recvFileThread)

    def closeEvent(self, event):
        self.runFlag = 0
        if self.sock:
            print "closing socket..."
            self.sock.close()
        self.close()

    def session(self, first_msg):
        # 离线消息，或者第一条消息
        print u"进入 session函数"
        if isinstance(first_msg, list):
            for i in range(0, len(first_msg), 2):
                print u"%s from %s" % (first_msg, self.fnick)
                self.ui.textBrowser.append(
                        u"<font color=red><b>[%s ] %s</b></font>" % (
                            self.fnick, first_msg[i]))
                self.ui.textBrowser.append(first_msg[i+1].decode('utf-8'))
        elif len(first_msg) > 0:
            print u"%s from %s" % (first_msg, self.fnick)
            self.ui.textBrowser.append(
                    u"<font color=red><b>[%s ] %s</b></font>" % (
                        self.fnick, self.curTime()[1]))
            self.ui.textBrowser.append(first_msg.decode('utf-8'))
        # 可下载的文件列表，包括A->B，或B->A的文件
        files = net.getFileLists(self.user_no, self.fno, self.srv_ip)
        fset = set()
        for fname in files:
            if len(fname) > 0 and fname != 'NONE':
                fset.add(fname)
        for fname in fset:
            self.ui.listWidgetFile.addItem(u"%s" % fname)
        inputs = [self.sock]
        outputs = [self.sock]
        # print u"重大bug"
        while self.runFlag:
            readable, writable, exceptional = \
                    select.select(inputs, outputs, inputs, 0.1)
            for s in readable:
                data = s.recv(1024)
                if data:
                    print u"%s from %s" % (data, str(s.getpeername()))
                    if data[0:6] == 'FILE\r\n':
                        rd = data[6:].split('|')
                        self.ui.listWidgetFile.addItem(rd[1])
                        data = u"%s正向你发送文件: %s" % (rd[0], rd[1])

                    self.ui.textBrowser.append(
                            u"<font color=red><b>[%s ] %s</b></font>" % (
                                self.fnick, self.curTime()[1]))
                    self.ui.textBrowser.append(data.decode('utf-8'))
            for s in writable:
                try:
                    msg = self.sMsgQueue.get_nowait()
                    # s.send(msg)
                    # print self.user_no, self.fno, msg
                    net.sendMsg(s, self.user_no, self.fno, msg)
                except Queue.Empty:
                    pass

    def curTime(self):
        return time.strftime('%Y-%m-%d %X',
                             time.localtime(time.time())).split(' ')

    def sendMsg(self):
        msg = self.ui.textEdit.toPlainText()
        self.ui.textEdit.clear()
        self.ui.textBrowser.append(
                u"<font color=blue><b>[%s ] %s</b></font>" % (
                    self.nick, self.curTime()[1]))
        self.ui.textBrowser.append(msg)
        self.sMsgQueue.put(msg)

    def sendFileThread(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
                self, "Open text file", "Open new file",
                self.tr("All Files (*.*)"))
        if fileName.isEmpty():
            print u"没有选择文件"
            return
        t = threading.Thread(target=self.sendFile, args=(fileName,))
        t.start()

    def sendFile(self, fileName):
        # send a file
        self.ui.textBrowser.append(u"正在发送 "+fileName+u"...")
        self.ui.listWidgetFile.addItem(fileName)
        ret = net.sendFile(self.user_no, self.fno, fileName, self.srv_ip)
        self.ui.textBrowser.append(u"%s" % ret)

    def recvFileThread(self):
        items = self.ui.listWidgetFile.selectedItems()
        for item in items:
            initialPath = QtCore.QDir.currentPath() + "/" + str(item.text())
            fileName = QtGui.QFileDialog.getSaveFileName(
                    self, "Save As", initialPath, "Files (*.*);;All Files (*)")
            if fileName.isEmpty():
                # print "not select file"
                return
            t = threading.Thread(target=self.recvFile,
                                 args=(fileName, str(item.text())))
            t.start()

    def recvFile(self, savedFileName, itemName):
        net.recvFile(savedFileName, itemName, self.srv_ip)
        self.ui.textBrowser.append("<font color=blue>[%s ] %s</font>" % (
                                   self.nick, self.curTime()[1]))
        self.ui.textBrowser.append(
                u"%s接收成功，保存在%s" % (itemName, savedFileName))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myqq = LoginDialog()
    myqq.show()
    sys.exit(app.exec_())
