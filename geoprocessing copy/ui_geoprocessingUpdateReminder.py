# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'geoprocessingUpdateReminder.ui'
#
# Created: Fri May 30 17:21:26 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_GeoprocessingUpdateReminder(object):
    def setupUi(self, GeoprocessingUpdateReminder):
        GeoprocessingUpdateReminder.setObjectName("GeoprocessingUpdateReminder")
        GeoprocessingUpdateReminder.setWindowModality(QtCore.Qt.WindowModal)
        GeoprocessingUpdateReminder.resize(QtCore.QSize(QtCore.QRect(0,0,511,150).size()).expandedTo(GeoprocessingUpdateReminder.minimumSizeHint()))
        GeoprocessingUpdateReminder.setMinimumSize(QtCore.QSize(511,150))
        GeoprocessingUpdateReminder.setMaximumSize(QtCore.QSize(511,150))

        self.label = QtGui.QLabel(GeoprocessingUpdateReminder)
        self.label.setGeometry(QtCore.QRect(9,25,493,21))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")

        self.label_2 = QtGui.QLabel(GeoprocessingUpdateReminder)
        self.label_2.setGeometry(QtCore.QRect(10,50,493,19))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")

        self.btnYes = QtGui.QPushButton(GeoprocessingUpdateReminder)
        self.btnYes.setGeometry(QtCore.QRect(262,100,91,29))
        self.btnYes.setObjectName("btnYes")

        self.btnNo = QtGui.QPushButton(GeoprocessingUpdateReminder)
        self.btnNo.setWindowModality(QtCore.Qt.NonModal)
        self.btnNo.setGeometry(QtCore.QRect(372,100,101,29))
        self.btnNo.setObjectName("btnNo")

        self.checkBox = QtGui.QCheckBox(GeoprocessingUpdateReminder)
        self.checkBox.setGeometry(QtCore.QRect(20,100,161,24))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(GeoprocessingUpdateReminder)
        QtCore.QMetaObject.connectSlotsByName(GeoprocessingUpdateReminder)

    def retranslateUi(self, GeoprocessingUpdateReminder):
        GeoprocessingUpdateReminder.setWindowTitle(QtGui.QApplication.translate("GeoprocessingUpdateReminder", "Geoprocessing Update Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GeoprocessingUpdateReminder", "The PyQgis Repository keeps a newer release of Geoprocessing for you.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("GeoprocessingUpdateReminder", "Do you want to upgrade?", None, QtGui.QApplication.UnicodeUTF8))
        self.btnYes.setText(QtGui.QApplication.translate("GeoprocessingUpdateReminder", "Upgrade", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNo.setText(QtGui.QApplication.translate("GeoprocessingUpdateReminder", "Upgrade later", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("GeoprocessingUpdateReminder", "disable this Feature", None, QtGui.QApplication.UnicodeUTF8))

