# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created: Thu Apr 17 21:36:07 2014
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

class Ui_DialogRegister(object):
    def __init__(self, DialogRegister):
        DialogRegister.setObjectName(_fromUtf8("DialogRegister"))
        DialogRegister.resize(271, 250)
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
        DialogRegister.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        DialogRegister.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pic/img/avatar.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogRegister.setWindowIcon(icon)
        DialogRegister.setAutoFillBackground(False)
        DialogRegister.setStyleSheet(_fromUtf8("background-color: rgb(85, 170, 255);"))
        self.label = QtGui.QLabel(DialogRegister)
        self.label.setGeometry(QtCore.QRect(30, 30, 54, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(DialogRegister)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 54, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(DialogRegister)
        self.label_3.setGeometry(QtCore.QRect(30, 160, 54, 12))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_srv = QtGui.QLineEdit(DialogRegister)
        self.lineEdit_srv.setGeometry(QtCore.QRect(80, 30, 161, 21))
        self.lineEdit_srv.setObjectName(_fromUtf8("lineEdit_srv"))
        self.lineEdit_usr = QtGui.QLineEdit(DialogRegister)
        self.lineEdit_usr.setGeometry(QtCore.QRect(80, 110, 161, 21))
        self.lineEdit_usr.setObjectName(_fromUtf8("lineEdit_usr"))
        self.lineEdit_pas = QtGui.QLineEdit(DialogRegister)
        self.lineEdit_pas.setGeometry(QtCore.QRect(80, 150, 161, 21))
        self.lineEdit_pas.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_pas.setObjectName(_fromUtf8("lineEdit_pas"))
        self.pushButton_reg = QtGui.QPushButton(DialogRegister)
        self.pushButton_reg.setGeometry(QtCore.QRect(30, 210, 211, 23))
        self.pushButton_reg.setObjectName(_fromUtf8("pushButton_reg"))
        self.lineEdit_eml = QtGui.QLineEdit(DialogRegister)
        self.lineEdit_eml.setGeometry(QtCore.QRect(80, 70, 161, 21))
        self.lineEdit_eml.setObjectName(_fromUtf8("lineEdit_eml"))
        self.label_4 = QtGui.QLabel(DialogRegister)
        self.label_4.setGeometry(QtCore.QRect(30, 70, 41, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_error = QtGui.QLabel(DialogRegister)
        self.label_error.setGeometry(QtCore.QRect(80, 185, 141, 21))
        self.label_error.setText(_fromUtf8(""))
        self.label_error.setObjectName(_fromUtf8("label_error"))

        self.retranslateUi(DialogRegister)
        QtCore.QMetaObject.connectSlotsByName(DialogRegister)

        self.Dialog = DialogRegister

    def retranslateUi(self, DialogRegister):
        DialogRegister.setWindowTitle(_translate("DialogRegister", "注册", None))
        self.label.setText(_translate("DialogRegister", "服务器", None))
        self.label_2.setText(_translate("DialogRegister", "昵称", None))
        self.label_3.setText(_translate("DialogRegister", "口令", None))
        self.pushButton_reg.setText(_translate("DialogRegister", "注册", None))
        self.label_4.setText(_translate("DialogRegister", "邮箱", None))

import img_rc
