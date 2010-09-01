import sys

# Importing the necessary Qt classes.

from PyQt4.QtGui import QLabel, QApplication

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

# We use the from foo import * syntax here because
# all of Qt's objects begin with a Q
# and thus we shouldn't run into namespace problems.

if __name__=='__main__':

	App = QApplication(sys.argv)
	
	# All Qt programs need an
	# QApplication instance.
	

	
	App.exec_()
	
	# Notice the _ after exec, this is to
	# avoid the confusion with Python's
	# exec() built-in-function
	
	# exec_() starts the main application
	# loop. Something like main() of other
	# toolkits.
