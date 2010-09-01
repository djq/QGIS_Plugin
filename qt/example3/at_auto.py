# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'at.ui'
#
# Created: Thu Aug  5 09:56:06 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.command = QtGui.QLineEdit(Dialog)
        self.command.setGeometry(QtCore.QRect(60, 40, 113, 22))
        self.command.setObjectName("command")
        self.schedule = QtGui.QPushButton(Dialog)
        self.schedule.setGeometry(QtCore.QRect(60, 70, 114, 32))
        self.schedule.setObjectName("schedule")
        self.time = QtGui.QDateTimeEdit(Dialog)
        self.time.setGeometry(QtCore.QRect(60, 130, 194, 25))
        self.time.setObjectName("time")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.schedule.setText(QtGui.QApplication.translate("Dialog", "schedule", None, QtGui.QApplication.UnicodeUTF8))

