# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/var/vhosts/pyqgis/builder/build/urbananalysis/Ui_UrbanAnalysis.ui'
#
# Created: Wed Jun 23 13:58:54 2010
#      by: PyQt4 UI code generator 4.4.4
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

        self.retranslateUi(UrbanAnalysis)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), UrbanAnalysis.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), UrbanAnalysis.reject)
        QtCore.QMetaObject.connectSlotsByName(UrbanAnalysis)

    def retranslateUi(self, UrbanAnalysis):
        UrbanAnalysis.setWindowTitle(QtGui.QApplication.translate("UrbanAnalysis", "UrbanAnalysis", None, QtGui.QApplication.UnicodeUTF8))

