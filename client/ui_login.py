# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Thu Apr 17 21:16:13 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_DialogLogin(object):
    def __init__(self, DialogLogin):
        DialogLogin.setObjectName(_fromUtf8("DialogLogin"))
        DialogLogin.resize(290, 222)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        DialogLogin.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        DialogLogin.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pic/img/avatar.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogLogin.setWindowIcon(icon)
        DialogLogin.setAutoFillBackground(False)
        DialogLogin.setStyleSheet(_fromUtf8("background-color: rgb(85, 170, 255);"))
        self.label = QtGui.QLabel(DialogLogin)
        self.label.setGeometry(QtCore.QRect(30, 30, 54, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(DialogLogin)
        self.label_2.setGeometry(QtCore.QRect(30, 71, 54, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(DialogLogin)
        self.label_3.setGeometry(QtCore.QRect(30, 121, 54, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_srv = QtGui.QLineEdit(DialogLogin)
        self.lineEdit_srv.setGeometry(QtCore.QRect(80, 30, 161, 21))
        self.lineEdit_srv.setObjectName(_fromUtf8("lineEdit_srv"))
        self.lineEdit_usr = QtGui.QLineEdit(DialogLogin)
        self.lineEdit_usr.setGeometry(QtCore.QRect(80, 70, 161, 21))
        self.lineEdit_usr.setObjectName(_fromUtf8("lineEdit_usr"))
        self.lineEdit_pas = QtGui.QLineEdit(DialogLogin)
        self.lineEdit_pas.setGeometry(QtCore.QRect(80, 120, 161, 21))
        self.lineEdit_pas.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_pas.setObjectName(_fromUtf8("lineEdit_pas"))
        self.pushButton_log = QtGui.QPushButton(DialogLogin)
        self.pushButton_log.setGeometry(QtCore.QRect(130, 180, 111, 23))
        self.pushButton_log.setObjectName(_fromUtf8("pushButton_log"))
        self.pushButton_reg = QtGui.QPushButton(DialogLogin)
        self.pushButton_reg.setGeometry(QtCore.QRect(30, 180, 61, 23))
        self.pushButton_reg.setObjectName(_fromUtf8("pushButton_reg"))
        self.label_error = QtGui.QLabel(DialogLogin)
        self.label_error.setGeometry(QtCore.QRect(80, 155, 141, 21))
        self.label_error.setText(_fromUtf8(""))
        self.label_error.setObjectName(_fromUtf8("label_error"))

        self.retranslateUi(DialogLogin)
        QtCore.QMetaObject.connectSlotsByName(DialogLogin)

        self.Dialog = DialogLogin

    def retranslateUi(self, DialogLogin):
        DialogLogin.setWindowTitle(_translate("DialogLogin", "登录", None))
        self.label.setText(_translate("DialogLogin", "服务器", None))
        self.label_2.setText(_translate("DialogLogin", "OC号", None))
        self.label_3.setText(_translate("DialogLogin", "口令", None))
        self.pushButton_log.setText(_translate("DialogLogin", "登录", None))
        self.pushButton_reg.setText(_translate("DialogLogin", "注册", None))

import img_rc
