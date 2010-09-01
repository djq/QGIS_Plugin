# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_UrbanAnalysis.ui'
#
# Created: Wed Jul  7 14:45:26 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_UrbanAnalysis(object):
    def setupUi(self, UrbanAnalysis):
        UrbanAnalysis.setObjectName("UrbanAnalysis")
        UrbanAnalysis.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(UrbanAnalysis)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.radioButton = QtGui.QRadioButton(UrbanAnalysis)
        self.radioButton.setGeometry(QtCore.QRect(20, 180, 101, 20))
        self.radioButton.setObjectName("radioButton")
        self.toolButton = QtGui.QToolButton(UrbanAnalysis)
        self.toolButton.setGeometry(QtCore.QRect(30, 40, 151, 41))
        self.toolButton.setObjectName("toolButton")

        self.retranslateUi(UrbanAnalysis)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), UrbanAnalysis.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), UrbanAnalysis.reject)
        QtCore.QMetaObject.connectSlotsByName(UrbanAnalysis)

    def retranslateUi(self, UrbanAnalysis):
        UrbanAnalysis.setWindowTitle(QtGui.QApplication.translate("UrbanAnalysis", "UrbanAnalysis", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("UrbanAnalysis", "Click me", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("UrbanAnalysis", "...", None, QtGui.QApplication.UnicodeUTF8))

