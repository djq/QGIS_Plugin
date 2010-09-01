import sys

# Importing the necessary Qt classes.

from PyQt4.QtGui import QLabel, QApplication

# We use the from foo import * syntax here because
# all of Qt's objects begin with a Q
# and thus we shouldn't run into namespace problems.

if __name__=='__main__':

	App = QApplication(sys.argv)
	
	# All Qt programs need an
	# QApplication instance.
	
	# We pass the sys.argv as its arguments
	# because Qt is adept at handling some
	# of the default command-line options
	# like style, size, etc by itself.
	
	Label = QLabel( "Hello World!" )
	
	# QLabel is the class providing a
	# simple label
	
	Label.show()
	
	# Like in most GUI toolkits, we have
	# to manually set it to show
	
	App.exec_()
	
	# Notice the _ after exec, this is to
	# avoid the confusion with Python's
	# exec() built-in-function
	
	# exec_() starts the main application
	# loop. Something like main() of other
	# toolkits.
